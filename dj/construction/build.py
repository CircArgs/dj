"""Functions to add to an ast DJ node queries"""

from dataclasses import dataclass, field
from itertools import chain
from typing import Dict, Generator, Iterable, List, Optional, Set, Tuple, Union, cast

from sqlmodel import Session

from dj.errors import DJError, DJException, ErrorCode
from dj.models.node import Node, NodeType
from dj.sql.parsing.ast import (
    Alias,
    Node as ASTNode,
    Column,
    Expression,
    Named,
    Name,
    Namespace,
    Query,
    Select,
    Table,
    TableExpression,
    BinaryOp,
    BinaryOpKind,
    Join,
    JoinKind,
)
from dj.sql.parsing.backends.sqloxide import parse
from dj.construction.compile import (
    ColumnDependencies,
    SelectDependencies,
    QueryDependencies,
)
from functools import reduce
from string import ascii_letters, digits

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


# flake8: noqa: C901
def build_select(
    session: Session,
    select: Select,
    deps: SelectDependencies,
    dialect: Optional[str] = None,
):
    # roll nodes up into categories
    # we roll up so we only handle a node once for all references
    dimension_columns: Dict[str, Tuple[Node, List[Column]]] = dict()
    transforms: Dict[str, Tuple[Node, List[Table]]] = dict()
    sources: Dict[str, Tuple[Node, List[Table]]] = dict()
    dimensions_tables: Dict[str, Tuple[Node, List[Table]]] = dict()

    for col, ref_node in deps.columns.all_columns:
        if isinstance(ref_node, Node) and ref_node.type == NodeType.DIMENSION:
            if ref_node.name in dimension_columns:
                dimension_columns[ref_node.name][1].append(col)
            else:
                dimension_columns[ref_node.name] = (ref_node, [col])

    for ref, ref_node in deps.tables:
        if ref_node.type == NodeType.DIMENSION:
            if ref_node.name in dimensions_tables:
                dimensions_tables[ref_node.name][1].append(ref)
            else:
                dimensions_tables[ref_node.name] = (ref_node, [ref])

        if ref_node.type == NodeType.SOURCE:
            if ref_node.name in sources:
                sources[ref_node.name][1].append(ref)
            else:
                sources[ref_node.name] = (ref_node, [ref])

        if ref_node.type == NodeType.TRANSFORM:
            if ref_node.name in transforms:
                transforms[ref_node.name][1].append(ref)
            else:
                transforms[ref_node.name] = (ref_node, [ref])

    # handle dimensions; join if needed
    for dim_name, (dim, cols) in dimension_columns.items():
        # if the dimension was not used as a table we will need to join
        if dim_name not in dimensions_tables:
            # alias used for the dimension throughout the query
            alias = amenable_name(dim.name)
            # find all sources, transforms and dimension tables that can join the dimension
            joinable = False
            join_info: Dict[str, Tuple[Node, List[Table]]] = {}
            # str, (DJ Node, [AST Table Node])
            for table_name, (table_node, tables) in chain(
                transforms.items(),
                sources.items(),
                dimensions_tables.items(),
            ):
                dim_cols = [col for col in table_node.columns if col.dimension == dim]
                join_info[table_name] = (
                    tables,
                    dim_cols,
                )
                if dim_cols:
                    joinable = True
            if not joinable:
                raise Exception(
                    f"""Dimension `{dim_name}` is not joinable. A SOURCE, TRANSFORM, or DIMENSION node which references this dimension must be used directly in the FROM clause:\n `{str(select.from_)}`.""",
                )

            dim_ast = Alias(Name(alias), child=parse(dim.query, dialect))

            # AST Column
            for col in cols:
                col.namespace = Namespace([Name(alias)])

            joins: List[Join] = []
            # [AST Table], [DJ Node Column]
            for tables, cols in join_info.values():
                for table in tables:
                    on = []
                    for col in cols:
                        on.append(
                            BinaryOp(
                                BinaryOpKind.Eq,
                                Column(Name(col.name), _table=table),
                                Column(
                                    Name(col.dimension_column),
                                    Namespace([Name(alias)]),
                                ),
                            ),
                        )
                joins.append(
                    Join(
                        JoinKind.LeftOuterdim,
                        dim_ast,
                        reduce(lambda l, r: BinaryOp(BinaryOpKind.And, l, r), on),
                    ),
                )

            select.from_.joins += joins

    # handle all nodes referenced as tables
    for node_name, (node, tables) in chain(
        transforms.items(),
        dimensions_tables.items(),
    ):
        alias = amenable_name(node.name)
        table_ast = Alias(Name(alias), child=parse(node.query, dialect))
        for exp, col in zip(table_ast.child.select.projection, node.columns):
            if not isinstance(exp, Named):
                to = Alias(Name(col.name), child = exp)
                exp.parent.replace(exp, to)
        for table in tables:
            parent = table.parent
            parent.replace(table, table_ast)
            # if not isinstance(
            #     parent,
            #     Alias,
            # ):  # if the table is not already aliased we will need to alias it and replace column refs
            #     for (
            #         col,
            #         node,
            #     ) in (
            #         deps.columns.all_columns
            #     ):  # find columns that referenced the table to replace their namespace
            #         if isinstance(node, ASTNode):
            #             if id(node) == id(table):
            #                 col.namespace = Namespace([Name(alias)])

    # We do not do anything about source nodes - for source, (source_node, table) in sources.items():

    for subquery, subquery_deps in deps.subqueries:
        build_select(session, subquery, subquery_deps, dialect)


def build_query(
    session: Session,
    query: Query,
    deps: QueryDependencies,
    dialect: Optional[str] = None,
):
    for cte in query.ctes:
        build_select(session, cte.child, deps.select, dialect)
    build_select(session, query.select, deps.select, dialect)
