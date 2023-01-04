"""
Functions for building queries, from nodes or SQL.
"""

from contextlib import contextmanager
from dataclasses import dataclass, field
from itertools import chain
from string import ascii_letters, digits
from typing import Dict, Generator, List, Optional, Set, Tuple, Union

from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from dj.models.node import Node, NodeType
from dj.sql.parsing.ast import (
    Alias,
    BinaryOp,
    BinaryOpKind,
    Column,
    Join,
    JoinKind,
    Name,
    Named,
    Namespace,
)
from dj.sql.parsing.ast import Node as ASTNode
from dj.sql.parsing.ast import Query, Select, Table, TableExpression, flatten
from dj.sql.parsing.backends.sqloxide import parse

ACCEPTABLE_CHARS = set(ascii_letters + digits + "_")
LOOKUP_CHARS = {
    ".": "DOT",
    "'": "QUOTE",
    '"': "DQUOTE",
    "`": "BTICK",
    "!": "EXCL",
    "@": "AT",
    "#": "HASH",
    "$": "DOLLAR",
    "%": "PERC",
    "^": "CARAT",
    "&": "AMP",
    "*": "STAR",
    "(": "LPAREN",
    ")": "RPAREN",
    "[": "LBRACK",
    "]": "RBRACK",
    "-": "MINUS",
    "+": "PLUS",
    "=": "EQ",
}


def amenable_name(name: str) -> str:
    """Takes a string and makes it have only alphanumerics/_"""
    ret = []
    cont = []
    for c in name:
        if c in ACCEPTABLE_CHARS:
            cont.append(c)
        elif c in LOOKUP_CHARS:
            ret.append("".join(cont))
            ret.append(LOOKUP_CHARS[c])
            cont = []
        else:
            ret.append("".join(cont))
            ret.append("_")
            cont = []

    return "_".join(ret) + "_" + "".join(cont)


def make_name(namespace, name="") -> str:
    """utility taking a namespace and name to make a possible name of a DJ Node"""
    ret = ""
    if namespace:
        ret += ".".join(name.name for name in namespace.names)
    if name:
        ret += ("." if ret else "") + name
    return ret


class BuildException(Exception):
    """Generic DJ Build Exception"""


class InvalidSQLException(BuildException):
    """Something is structurally wrong with query"""

    def __init__(self, message: str, node: ASTNode, context: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        self.context = context

    def __str__(self) -> str:
        ret = f"{self.message} `{self.node}`"
        if self.context:
            ret += f" from `{self.context}`"
        return ret


class MissingColumnException(BuildException):
    """Column cannot be resolved in query"""

    def __init__(self, message: str, column: Column, context: Optional[ASTNode] = None):
        self.message = message
        self.column = column
        self.context = context

    def __str__(self) -> str:
        ret = f"{self.message} `{self.column}`"
        if self.context:
            ret += f" from `{self.context}`"
        return ret


class UnknownNodeException(BuildException):
    """Node in query does not exist"""

    def __init__(self, message: str, node: str, context: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        self.context = context

    def __str__(self) -> str:
        ret = self.message
        if self.context:
            ret += f" from:\n\n `{self.context}`"
        return ret


class NodeTypeException(BuildException):
    """Node is the wrong type"""

    def __init__(self, message: str, node: str, context: Optional[ASTNode] = None):
        self.message = message
        self.node = node
        self.context = context

    def __str__(self) -> str:
        ret = self.message
        if self.context:
            ret += f" from:\n\n `{self.context}`"
        return ret


class CompoundBuildException(BuildException):
    _instance: Optional["CompoundBuildException"] = None
    _raise: bool = True
    errors: List[BuildException]

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CompoundBuildException, cls).__new__(
                cls, *args, **kwargs
            )
            cls.errors = []
        return cls._instance

    def reset(self):
        self._raise = True
        self.errors = []

    def clear(self):
        self.errors = []

    def set_raise(self, raise_: bool):
        self._raise = raise_

    @property  # type: ignore
    @contextmanager
    def catch(self):
        try:
            yield
        except BuildException as exc:
            if not self._raise:
                self.errors.append(exc)
            else:
                raise exc

    def __str__(self) -> str:
        plural = "s" if len(self.errors) > 1 else ""
        error = f"Found {len(self.errors)} issue{plural}:\n"
        return error + "\n\n".join(
            "\t" + str(type(exc).__name__) + ": " + str(exc) + "\n" + "=" * 50
            for exc in self.errors
        )


def get_dj_node(
    session: Session,
    node_name: str,
    kinds: Optional[Set[NodeType]] = None,
) -> Optional[Node]:
    """Return the DJ Node with a given name from a set of node types"""
    query = select(Node).filter(Node.name == node_name)
    match = None
    try:
        match = session.exec(query).one()
    except NoResultFound as exc:
        with CompoundBuildException().catch:
            kind_msg = " or ".join(str(k) for k in kinds) if kinds else ""
            raise UnknownNodeException(
                f"No {kind_msg} node `{node_name}` exists.",
                node_name,
            ) from exc

    if match and kinds and (match.type not in kinds):
        with CompoundBuildException().catch:
            raise NodeTypeException(
                f"Node `{match.name}` is of type `{str(match.type).upper()}`. Expected kind to be of {' or '.join(str(k) for k in kinds)}.",  # pylint: disable=C0301
                node_name,
            )

    return match


@dataclass
class ColumnDependencies:
    """Columns discovered from a query"""

    projection: List[Tuple[Column, TableExpression]] = field(
        default_factory=list,
    )  # selected nodes
    group_by: List[Tuple[Column, Union[TableExpression, Node]]] = field(
        default_factory=list,
    )
    filters: List[Tuple[Column, Union[TableExpression, Node]]] = field(
        default_factory=list,
    )  # where/having
    ons: List[Tuple[Column, Union[TableExpression, Node]]] = field(
        default_factory=list,
    )  # join ons

    @property
    def all_columns(
        self,
    ) -> Generator[Tuple[Column, Union[TableExpression, Node]], None, None]:
        for pair in chain(
            iter(self.projection),
            iter(self.group_by),
            iter(self.filters),
            iter(self.ons),
        ):
            yield pair


@dataclass
class SelectDependencies:
    tables: List[Tuple[TableExpression, Node]] = field(default_factory=list)
    columns: ColumnDependencies = field(default_factory=ColumnDependencies)
    subqueries: List[Tuple[Select, "SelectDependencies"]] = field(default_factory=list)

    @property
    def all_tables(self) -> Generator[Tuple[TableExpression, Node], None, None]:
        for t in self.tables:
            yield t
        for _, s in self.subqueries:
            for t in s.all_tables:
                yield t

    @property
    def all_node_dependencies(self) -> Set[Node]:
        return {node for _, node in self.all_tables if isinstance(node, Node)} | {
            node for _, node in self.columns.all_columns if isinstance(node, Node)
        }


@dataclass
class QueryDependencies:
    ctes: List[SelectDependencies] = field(default_factory=list)
    select: SelectDependencies = field(default_factory=SelectDependencies)

    @property
    def all_node_dependencies(self) -> Set[Node]:
        ret = self.select.all_node_dependencies
        for cte_deps in self.ctes:
            ret |= cte_deps.all_node_dependencies
        return ret


# flake8: noqa: C901
def extract_dependencies_from_select(
    session: Session,
    select: Select,
) -> SelectDependencies:
    # first, we get the tables in the from of the select including subqueries
    # we take stock of the columns that can come from said tables
    # then we check the select, groupby,
    # having/where for the columns keeping track of where they came from

    table_deps = SelectDependencies()

    # depth 1 tables
    tables = select.from_.tables + [join.table for join in select.from_.joins]

    # namespaces track the namespace: list of columns that can be had from it
    namespaces: Dict[str, Set[str]] = dict()

    # namespace: ast node defining namespace
    table_nodes: Dict[str, TableExpression] = dict()

    # track subqueries encountered to extract from them after
    subqueries: List[Select] = []

    # used to check need and capacity for merging in dimensions
    dimension_columns: Set[Node] = set()
    sources_transforms: Set[Node] = set()
    dimensions_tables: Set[Node] = set()

    # get all usable namespaces and columns from the tables
    for table in tables:
        namespace = ""
        if isinstance(table, Named):
            namespace = make_name(table.namespace, table.name.name)

        # you cannot combine an unnamed subquery with anything else
        if (namespace and "" in namespaces) or (namespace == "" and namespaces):
            with CompoundBuildException().catch:
                raise InvalidSQLException(
                    "You may only use an unnamed subquery alone.",
                    table,
                )

        # you cannot have multiple references with the same name
        if namespace in namespaces:
            with CompoundBuildException().catch:
                raise InvalidSQLException(
                    f"Duplicate name `{namespace}` for table.",
                    table,
                )

        namespaces[namespace] = set()

        if isinstance(table, Alias):
            table = table.child  # type: ignore

        # subquery handling
        # we track subqueries separately and extract at the end
        # but introspect the columns to make sure the parent query selection is valid
        if isinstance(table, Query):
            if table.ctes:
                with CompoundBuildException().catch:
                    raise InvalidSQLException("ctes are not allowed here", table)

            subqueries.append(table.select)

            for col in table.select.projection:
                if not isinstance(col, Named):
                    with CompoundBuildException().catch:
                        raise InvalidSQLException(
                            f"{col} is an unnamed expression. Try adding an alias.",
                            col,
                            table.select,
                        )

                namespaces[namespace].add(col.name.name)
        # tables are sought as nodes and nothing else
        # can be source, transform, dimension
        elif isinstance(table, Table):
            node_name = make_name(table.namespace, table.name.name)
            table_node = get_dj_node(
                session,
                node_name,
                {NodeType.SOURCE, NodeType.TRANSFORM, NodeType.DIMENSION},
            )
            if table_node is not None:
                namespaces[namespace] |= {c.name for c in table_node.columns}
                table_deps.tables.append((table, table_node))
                if table_node.type in {NodeType.SOURCE, NodeType.TRANSFORM}:
                    sources_transforms.add(table_node)
        table_nodes[namespace] = table

    # organize column discovery recording dupes
    # we'll use this lookup to validate columns
    no_namespace_safe_cols = set()
    multiple_refs = set()
    for namespaces_cols in namespaces.values():
        for col in namespaces_cols:  # type: ignore
            if col in no_namespace_safe_cols:
                multiple_refs.add(col)
            no_namespace_safe_cols.add(col)

    namespaces[""] = no_namespace_safe_cols - multiple_refs  # type: ignore

    def check_col(col: Column, add: list) -> Optional[str]:
        """Check if a column can be had in a query"""
        namespace = make_name(col.namespace)  # str preceding the column name
        cols = namespaces.get(namespace)
        if cols is None:
            with CompoundBuildException().catch:
                raise MissingColumnException(
                    f"No namespace `{namespace}` from which to reference column `{col.name.name}`.",
                    col,
                    col.parent,
                )

            return None
        elif col.name.name not in cols:
            exc_msg = f"Namespace `{namespace}` has no column `{col.name.name}`."
            if not namespace:
                exc_msg = (
                    f"Column `{col.name.name}` does not exist in any referenced tables."
                )
                if col.name.name in multiple_refs:
                    exc_msg = f"`{col.name.name}` appears in multiple references and so must be namespaced."  # pylint: disable=C0301
            with CompoundBuildException().catch:
                raise MissingColumnException(exc_msg, col, col.parent)

            return None
        elif namespace:
            add.append((col, table_nodes[namespace]))
        else:
            for k, v in namespaces.items():
                if col.name.name in v:
                    add.append((col, table_nodes[k]))
                    break
        return namespace

    # check projection
    for col in chain(*(exp.find_all(Column) for exp in select.projection)):
        check_col(col, table_deps.columns.projection)  # type: ignore

    # check groupby, filters, and join ons
    gbfo: List[
        Tuple[List[Tuple[Column, Union[TableExpression, Node]]], Column, bool]
    ] = []

    if select.group_by:
        gbfo += [
            (table_deps.columns.group_by, col, True)
            for col in chain(*(exp.find_all(Column) for exp in select.group_by))
        ]
        if select.having:
            gbfo += [
                (table_deps.columns.filters, col, True)
                for col in select.having.find_all(Column)
            ]
    elif select.having:
        with CompoundBuildException().catch:
            raise InvalidSQLException(
                "HAVING without a GROUP BY is not allowed. Use WHERE instead.",
                select.having,
                select,
            )

    if select.where:
        gbfo += [
            (table_deps.columns.filters, col, True)
            for col in select.where.find_all(Column)
        ]

    if select.from_.joins:
        for join in select.from_.joins:
            gbfo += [
                (table_deps.columns.ons, col, False) for col in join.on.find_all(Column)
            ]

    for add, col, dim_allowed in gbfo:
        bad_namespace = False
        try:
            namespace = check_col(col, add)  # type: ignore
            bad_namespace = namespace is None
        except BuildException:
            bad_namespace = True
        if bad_namespace:
            namespace = make_name(col.namespace)
            if not dim_allowed:
                with CompoundBuildException().catch:
                    raise InvalidSQLException(
                        "Cannot reference a dimension here.",
                        col,
                        col.parent,
                    )

            else:
                dim = get_dj_node(session, namespace, {NodeType.DIMENSION})
                if (dim is not None) and (
                    col.name.name not in {c.name for c in dim.columns}
                ):
                    with CompoundBuildException().catch:
                        raise MissingColumnException(
                            f"Dimension `{dim.name}` has no column `{col.name.name}`.",
                            col,
                            col.parent,
                        )

                    add.append((col, dim))
                    dimension_columns.add(dim)

    # check if there are any column dimension dependencies we need to join but cannot
    # if a dimension is already used directly in the from (manually join or ref'd) -
    # - there is no need to join it so we check only dimensions not used that way
    for dim in dimension_columns - dimensions_tables:
        joinable = False
        for st in sources_transforms:
            for col in st.columns:
                if st.dimension == dim:
                    joinable = True
                    break
            if joinable:
                break
        if not joinable:
            with CompoundBuildException().catch:
                NodeTypeException(
                    f"Dimension `{dim.name}` is not joinable. A SOURCE, TRANSFORM, or DIMENSION node which references this dimension must be used directly in the FROM clause.",  # pylint: disable=C0301
                    dim,
                    select.from_,
                )

    for subquery in subqueries:
        table_deps.subqueries.append(
            (
                subquery,
                extract_dependencies_from_select(session, subquery),
            ),
        )

    return table_deps


def extract_dependencies_from_query(
    session: Session,
    query: Query,
) -> QueryDependencies:
    return QueryDependencies(
        select=extract_dependencies_from_select(session, query.select),
    )


def extract_dependencies(
    session: Session,
    node: Node,
    dialect: Optional[str] = None,
    raise_: bool = True,
    distance: int = -1,
) -> Tuple[Set[Node], Set[str]]:
    """Find all dependencies in the dj dag of a node

    distance: how many steps away to explore.
        <0 infinitely far,
        0 only neighbors e.g. only nodes referenced directly in the node query
    """
    _distance = float("inf") if distance < 0 else float(distance)
    if node.query is None:
        raise Exception("Node has no query")
    ast = parse(node.query, dialect)
    CompoundBuildException().reset()
    CompoundBuildException().set_raise(False)
    deps: QueryDependencies = extract_dependencies_from_query(session, ast)
    dep_nodes: Tuple[Set[Node], Set[str]] = (deps.all_node_dependencies, set())
    added = True
    travelled = 0
    new: Tuple[Set[Node], Set[str]] = (set(), set())
    while added and travelled < _distance:
        for dep_node in dep_nodes[0]:
            if dep_node.type != NodeType.SOURCE:
                extract = extract_dependencies(session, dep_node, dialect)
                new = (new[0] | extract[0], new[1] | extract[1])
        curr_len = len(dep_nodes)
        dep_nodes = (new[0] | dep_nodes[0], new[1] | dep_nodes[1])
        if curr_len != len(dep_nodes):
            added = True
        else:
            added = False
        travelled += 1

    if CompoundBuildException().errors and raise_:
        raise CompoundBuildException()

    for exc in CompoundBuildException().errors:
        if isinstance(exc, (UnknownNodeException, NodeTypeException)):
            dep_nodes[1].add(exc.node)

    return dep_nodes


# # flake8: noqa: C901
# def build_select(
#     session: Session,
#     select: Select,
#     deps: SelectDependencies,
#     dialect: Optional[str] = None,
# ):
#     # roll nodes up into categories
#     # we roll up so we only handle a node once for all references
#     dimension_columns: Dict[str, Tuple[Node, List[Column]]] = dict()
#     transforms: Dict[str, Tuple[Node, List[Table]]] = dict()
#     sources: Dict[str, Tuple[Node, List[Table]]] = dict()
#     dimensions_tables: Dict[str, Tuple[Node, List[Table]]] = dict()

#     for col, ref_node in deps.columns.all_columns:
#         if isinstance(ref_node, Node) and ref_node.type == NodeType.DIMENSION:
#             if ref_node.name in dimension_columns:
#                 dimension_columns[ref_node.name][1].append(col)
#             else:
#                 dimension_columns[ref_node.name] = (ref_node, [col])

#     for ref, ref_node in deps.tables:
#         if ref_node.type == NodeType.DIMENSION:
#             if ref_node.name in dimensions_tables:
#                 dimensions_tables[ref_node.name][1].append(ref)
#             else:
#                 dimensions_tables[ref_node.name] = (ref_node, [ref])

#         if ref_node.type == NodeType.SOURCE:
#             if ref_node.name in sources:
#                 sources[ref_node.name][1].append(ref)
#             else:
#                 sources[ref_node.name] = (ref_node, [ref])

#         if ref_node.type == NodeType.TRANSFORM:
#             if ref_node.name in transforms:
#                 transforms[ref_node.name][1].append(ref)
#             else:
#                 transforms[ref_node.name] = (ref_node, [ref])

#     # handle dimensions; join if needed
#     for dim_name, (dim, cols) in dimension_columns.items():
#         # if the dimension was not used as a table we will need to join
#         if dim_name not in dimensions_tables:
#             # alias used for the dimension throughout the query
#             alias = amenable_name(dim.name)
#             # find all sources, transforms and dimension tables that can join the dimension
#             joinable = False
#             join_info = dict()
#             # str, (DJ Node, [AST Table Node])
#             for table_name, (table_node, tables) in chain(
#                 transforms.items(),
#                 sources.items(),
#                 dimensions_tables.items(),
#             ):
#                 dim_cols = [col for col in table_node.columns if col.dimension == dim]
#                 join_info[table_name] = (
#                     tables,
#                     dim_cols,
#                 )
#                 if dim_cols:
#                     joinable = True
#             if not joinable:
#                 raise Exception(
#                     f"""Dimension `{dim_name}` is not joinable. A SOURCE, TRANSFORM, or DIMENSION node which references this dimension must be used directly in the FROM clause:\n `{str(select.from_)}`.""",
#                 )

#             dim_ast = Alias(Name(alias), child=parse(dim.query, dialect))

#             # AST Column
#             for col in cols:
#                 col.namespace = Namespace([Name(alias)])

#             joins: List[Join] = []
#             # [AST Table], [DJ Node Column]
#             for tables, cols in join_info.values():
#                 for table in tables:
#                     on = []
#                     for col in cols:
#                         on.append(
#                             BinaryOp(
#                                 BinaryOpKind.Eq,
#                                 Column(Name(col.name), _table=table),
#                                 Column(
#                                     Name(col.dimension_column),
#                                     Namespace([Name(alias)]),
#                                 ),
#                             ),
#                         )
#                 joins.append(
#                     Join(
#                         JoinKind.LeftOuterdim,
#                         dim_ast,
#                         reduce(lambda l, r: BinaryOp(BinaryOpKind.And, l, r), on),
#                     ),
#                 )

#             select.from_.joins += joins

#     # handle all nodes referenced as tables
#     for node_name, (node, tables) in chain(
#         transforms.items(),
#         dimensions_tables.items(),
#     ):
#         alias = amenable_name(node.name)
#         table_ast = Alias(Name(alias), child=parse(node.query, dialect))

#         for table in tables:
#             parent = table.parent
#             parent.replace(table, table_ast)
#             if not isinstance(
#                 parent,
#                 Alias,
#             ):  # if the table is not already aliased we will need to alias it and replace column refs
#                 for (
#                     col,
#                     node,
#                 ) in (
#                     deps.columns.all_columns
#                 ):  # find columns that referenced the table to replace their namespace
#                     if isinstance(node, ASTNode):
#                         if id(node) == id(table):
#                             col.namespace = Namespace([Name(alias)])

#     # We do not do anything about source nodes - for source, (source_node, table) in sources.items():

#     for subquery, subquery_deps in deps.subqueries:
#         build_select(session, subquery, subquery_deps, dialect)


# def build_query(
#     session: Session,
#     query: Query,
#     deps: QueryDependencies,
#     dialect: Optional[str] = None,
# ):
#     build_select(session, query.select, deps.select, dialect)


# @dataclass
# class DJQuery:
#     ast: Query
#     dependencies: QueryDependencies = field(default_factory=QueryDependencies)


# def build_node(session: Session, node: Node, dialect: Optional[str] = None) -> DJQuery:
#     query = parse(node.query, dialect)
#     CompoundBuildException().set_raise(True)
#     deps = extract_dependencies_from_query(session, query)
#     build_query(session, query, deps, dialect)
#     return DJQuery(query, deps)
