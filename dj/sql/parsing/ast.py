"""
Types to represent the DJ AST used as an intermediate representation for DJ operations
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, fields
from enum import Enum
from itertools import chain, zip_longest
from typing import (
    Any,
    Callable,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from dj.sql.parsing.backends.exceptions import DJParseException

PRIMITIVES = {int, float, str, bool, type(None)}


def flatten(maybe_iterables: Any) -> Iterator:
    """
    flattens `maybe_iterables` by descending into items that are Iterable
    """

    if not isinstance(maybe_iterables, (list, tuple, set, Iterator)):
        return iter([maybe_iterables])
    return chain.from_iterable(
        (flatten(maybe_iterable) for maybe_iterable in maybe_iterables)
    )


class DJEnum(Enum):
    """
    A DJ AST enum
    """

    def __repr__(self) -> str:
        return str(self)


# typevar used for node methods that return self
# so the typesystem can correlate the self type with the return type
TNode = TypeVar("TNode", bound="Node")  # pylint: disable=C0103


class Node(ABC):
    """Base class for all DJ AST nodes.

    DJ nodes are python dataclasses with the following patterns:
        - Attributes are either
            - PRIMITIVES (int, float, str, bool, None)
            - iterable from (list, tuple, set)
            - Enum
            - descendant of `Node`
        - Attributes starting with '_' are "obfuscated" and are not included in `children`

    """

    parent: Optional["Node"] = None

    def __post_init__(self):
        self.add_self_as_parent()

    def clear_parent(self: TNode) -> TNode:
        """remove parent from the node"""
        self.parent = None
        return self

    def set_parent(self: TNode, parent: "Node") -> TNode:
        """add parent to the node"""
        self.parent = parent
        return self

    def add_self_as_parent(self: TNode) -> TNode:
        """adds self as a parent to all children"""
        for child in self.children:
            child.set_parent(self)
        return self

    def __setattr__(self, key: str, value: Any):
        """Facilitates setting children using `.` syntax ensuring parent is attributed"""
        if key == "parent":
            object.__setattr__(self, key, value)
            return

        object.__setattr__(self, key, value)
        for child in flatten(value):
            if isinstance(child, Node) and not key.startswith("_"):
                child.set_parent(self)

    def get_nearest_parent_of_type(
        self: "Node",
        node_type: Type[TNode],
    ) -> Optional[TNode]:
        """traverse up the tree until you find a node of `node_type` or hit the root"""
        if isinstance(self.parent, node_type):
            return self.parent
        if self.parent is None:
            return None
        return self.parent.get_nearest_parent_of_type(node_type)

    def flatten(self) -> Iterator["Node"]:
        """flatten the sub-ast of the node as an iterator"""
        return self.filter(lambda _: True)

    def fields(
        self,
        flat: bool = True,
        nodes_only: bool = True,
        obfuscated: bool = False,
        nones: bool = False,
        named: bool = False,
    ) -> Iterator:
        """Returns an iterator over fields of a node with particular filters

        Args:
            flat: return a flattened iterator (if children are iterable)
            nodes_only: do not yield children that are not Nodes (trumped by `obfuscated`)
            obfuscated: yield fields that have leading underscores
                (typically accessed via a property)
            nones: yield values that are None
                (optional fields without a value); trumped by `nodes_only`
            named: yield pairs `(field name: str, field value)`; conflicts with flat
        Returns:
            Iterator: returns all children of a node given filters
                and optional flattening (by default Iterator[Node])
        """
        if flat and named:
            raise Exception("Cannot get fields `flat` and `named`.")

        def make_child_generator():
            """makes a generator enclosing self to return not obfuscated fields (fields without starting `_`)"""  # pylint: disable=C0301
            for self_field in fields(self):
                if not self_field.name.startswith("_") if not obfuscated else True:
                    if self_field.name in self.__dict__:
                        value = self.__dict__[self_field.name]
                        if named:
                            yield self_field.name, value
                        else:
                            yield value

        # `iter`s used to satisfy mypy (`child_generator` type changes between generator, filter)
        child_generator = iter(make_child_generator())
        if flat:
            child_generator = iter(flatten(child_generator))

        if nodes_only:
            child_generator = iter(
                filter(
                    lambda child: isinstance(child, Node)
                    if not named
                    else isinstance(child[1], Node),
                    child_generator,
                ),
            )

        if not nones:
            child_generator = iter(
                filter(
                    lambda child: (child is not None)
                    if not named
                    else (child[1] is not None),
                    child_generator,
                ),
            )  # pylint: disable=C0301

        return child_generator

    @property
    def children(self) -> Iterator["Node"]:
        """returns an iterator of all nodes that are one step from the current node down including through iterables"""  # pylint: disable=C0301
        return self.fields(
            flat=True,
            nodes_only=True,
            obfuscated=False,
            nones=False,
            named=False,
        )

    def replace(self: TNode, from_: "Node", to: "Node") -> TNode:
        """Replace a node `from_` with a node `to` in the subtree"""
        for name, child in self.fields(
            flat=False,
            nodes_only=False,
            obfuscated=True,
            nones=False,
            named=True,
        ):
            if isinstance(child, (list, tuple)):
                new = []
                for c in child:
                    if id(c) != id(from_):
                        new.append(c)
                    else:
                        new.append(to)
                    if isinstance(c, Node):
                        c.replace(from_, to)
                if isinstance(child, tuple):
                    new = tuple(new)  # type: ignore

                self.__setattr__(name, new)
            else:
                if id(child) == id(from_):
                    self.__setattr__(name, to)
            if isinstance(child, Node):
                child.replace(from_, to)

        return self

    def filter(self, func: Callable[["Node"], bool]) -> Iterator["Node"]:
        """find all nodes that `func` returns `True` for"""
        if func(self):
            yield self
        for node in chain(*[child.filter(func) for child in self.children]):
            yield node

    def find_all(self, node_type: Type[TNode]) -> Iterator[TNode]:
        """find all nodes of a particular type in the node's sub-ast"""
        return self.filter(lambda n: isinstance(n, node_type))  # type: ignore

    def apply(self, func: Callable[["Node"], None]):
        """
        traverse ast and apply func to each Node
        """
        func(self)
        for child in self.children:
            child.apply(func)

    def compare(self, other: "Node") -> bool:
        """a compare two ASTs"""

        return not self.diff(other)

    def diff(self, other: "Node") -> List[Tuple["Node", "Node"]]:
        """compare two ASTs for differences and return the pairs of differences"""

        def _diff(self, other: "Node"):
            if self != other:
                diffs.append((self, other))
            else:
                for child, other_child in zip_longest(self.children, other.children):
                    _diff(child, other_child)

        diffs: List[Tuple["Node", "Node"]] = []
        _diff(self, other)
        return diffs

    def __eq__(self, other) -> bool:
        """Compares two nodes for "top level" equality.

        Checks for type equality and primitive field types for full equality.
        Compares all others for type equality only. No recursing.
        Note: Does not check (sub)AST. See `Node.compare` for comparing (sub)ASTs.
        """
        return type(self) == type(other) and all(  # pylint: disable=C0123
            s == o
            if type(s) in PRIMITIVES  # pylint: disable=C0123
            else type(s) == type(o)  # pylint: disable=C0123
            for s, o in zip(
                (self.fields(False, False, False, True)),
                (other.fields(False, False, False, True)),
            )
        )

    @abstractmethod
    def __hash__(self) -> int:
        """hash a node"""

    @abstractmethod
    def __str__(self) -> str:
        """get the string of a node"""


TExpression = TypeVar(
    "TExpression",
    bound="Expression",
)  # pylint: disable=C0103


class Expression(Node):
    """an expression type simply for type checking"""

    def alias_or_self(self: TExpression) -> TExpression:
        """get the alias name of an expression if it is the descendant of an alias otherwise get its own name"""  # pylint: disable=C0301
        if isinstance(self.parent, Alias):
            return self.parent  # type: ignore
        return self


@dataclass(eq=False)
class Name(Node):
    """the string name specified in sql with quote style"""

    name: str
    quote_style: str = ""

    def to_named_type(self, named_type: Type["Named"]) -> "Named":
        """transform the name into a specific Named that only requires a name to create"""
        return named_type(self)

    def __hash__(self) -> int:
        return hash(self.name + self.quote_style)

    def __str__(self) -> str:
        return (
            f"{self.quote_style}{self.name}{self.quote_style}"  # pylint: disable=C0301
        )


TNamed = TypeVar("TNamed", bound="Named")  # pylint: disable=C0103


@dataclass(eq=False)
class Namespace(Node):
    """Represents a sequence of names prececeding some Table or Column"""

    names: List[Name]

    def to_named_type(self, named_type: Type[TNamed]) -> TNamed:
        """transform the namespace into a column whose name is the last name in the namespace

        if the namespace contains a single name,
            the created column will have no namespace
        otherwise, the remaining names for the column's namespace
        """
        if not self.names:
            raise DJParseException("Namespace is empty")
        converted = named_type(self.names.pop().clear_parent())
        if self.names:
            converted.add_namespace(self)
        return converted

    def pop_self(self) -> Tuple["Namespace", Name]:
        """a utility function that returns the last name and the remaining namespace as a tuple

        useful for parsing compound identifiers and revealing
        the last name for another attribute
        """
        last = self.names.pop().clear_parent()
        return self, last

    def __str__(self) -> str:
        return ".".join(str(name) for name in self.names)

    def __hash__(self) -> int:
        return hash(Namespace)


@dataclass(eq=False)  # type: ignore
class Named(Expression):
    """An Expression that has a name"""

    name: Name

    namespace: Optional[Namespace] = None

    def add_namespace(self: TNamed, namespace: Optional[Namespace]) -> TNamed:
        """add a namespace to the Table if one does not exist"""
        if self.namespace is None:
            self.namespace = namespace
        return self.add_self_as_parent()

    def alias_or_name(self) -> Name:
        """get the alias name of a node if it is the descendant of an alias otherwise get its own name"""  # pylint: disable=C0301
        return self.alias_or_self().name


class Operation(Expression):
    """a type to overarch types that operate on other expressions"""


# pylint: disable=C0103
class UnaryOpKind(DJEnum):
    """the accepted unary operations"""

    Plus = "+"
    Minus = "-"
    Not = "NOT"


# pylint: enable=C0103


@dataclass(eq=False)
class UnaryOp(Operation):
    """an operation that operates on a single expression"""

    op: UnaryOpKind  # pylint: disable=C0103
    expr: Expression

    def __hash__(self) -> int:
        return hash((UnaryOp, self.op))

    def __str__(self) -> str:
        return f"{self.op.value} {(self.expr)}"


# pylint: disable=C0103
class BinaryOpKind(DJEnum):
    """the DJ AST accepted binary operations"""

    And = "AND"
    Or = "OR"
    Is = "IS"
    Eq = "="
    NotEq = "<>"
    Gt = ">"
    Lt = "<"
    GtEq = ">="
    LtEq = "<="
    BitwiseOr = "|"
    BitwiseAnd = "&"
    BitwiseXor = "^"
    Multiply = "*"
    Divide = "/"
    Plus = "+"
    Minus = "-"
    Modulo = "%"


# pylint: enable=C0103


@dataclass(eq=False)
class BinaryOp(Operation):
    """represents an operation that operates on two expressions"""

    op: BinaryOpKind  # pylint: disable=C0103
    left: Expression
    right: Expression

    def __hash__(self) -> int:
        return hash((BinaryOp, self.op))

    def __str__(self) -> str:
        return f"{(self.left)} {self.op.value} {(self.right)}"


@dataclass(eq=False)
class Between(Operation):
    """a between statement"""

    expr: Expression
    low: Expression
    high: Expression

    def __hash__(self) -> int:
        return hash((Between, self.low, self.high))

    def __str__(self) -> str:
        return f"{(self.expr)} BETWEEN {(self.low)} AND {(self.high)}"


@dataclass(eq=False)
class Case(Expression):
    """a case statement of branches"""

    conditions: List[Expression] = field(default_factory=list)
    else_result: Optional[Expression] = None
    operand: Optional[Expression] = None
    results: List[Expression] = field(default_factory=list)

    def __hash__(self) -> int:
        return id(self)

    def __str__(self) -> str:
        branches = "\n\tWHEN ".join(
            f"{(cond)} THEN {(result)}"
            for cond, result in zip(self.conditions, self.results)
        )
        return f"""(CASE
        WHEN {branches}
        ELSE {(self.else_result)}
    END)"""


@dataclass(eq=False)
class Function(Named, Operation):
    """represents a function used in a statement"""

    args: List[Expression] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(Function)

    def __str__(self) -> str:
        return f"{self.name}({', '.join(str(arg) for arg in self.args)})"


@dataclass(eq=False)
class IsNull(Operation):
    """class representing IS NULL"""

    expr: Expression

    def __hash__(self) -> int:
        return hash(IsNull)

    def __str__(self) -> str:
        return f"{(self.expr)} IS NULL"


@dataclass(eq=False)  # type: ignore
class Value(Expression):
    """base class for all values number, string, boolean"""

    value: Union[str, bool, float, int]

    def __str__(self) -> str:
        if isinstance(self, String):
            return f"'{self.value}'"
        return str(self.value)


@dataclass(eq=False)
class Number(Value):
    """number value"""

    value: Union[float, int]

    def __post_init__(self):
        super().__post_init__()
        if type(self.value) not in (float, int):
            try:
                self.value = int(self.value)
            except ValueError:
                self.value = float(self.value)

    def __hash__(self) -> int:
        return hash((Number, self.value))


class String(Value):
    """string value"""

    value: str

    def __hash__(self) -> int:
        return hash((String, self.value))


class Boolean(Value):
    """boolean True/False value"""

    value: bool

    def __hash__(self) -> int:
        return hash((Boolean, self.value))


NodeType = TypeVar("NodeType", bound=Node)  # pylint: disable=C0103


@dataclass(eq=False)
class Alias(Named, Generic[NodeType]):
    """wraps node types with an alias"""

    child: Node = field(default_factory=Node)

    def __hash__(self) -> int:
        return hash((Alias, self.name))

    def __str__(self) -> str:
        return f"{self.child} AS {self.name}"


@dataclass(eq=False)
class Column(Named):
    """column used in statements"""

    _table: Optional["Table"] = field(repr=False, default=None)

    @property
    def table(self) -> Optional["Table"]:
        """return the table the column was referenced from"""
        return self._table

    def add_table(self, table: "Table") -> "Column":
        """add a referenced table"""
        if self._table is None:
            self._table = table
        return self

    def __hash__(self) -> int:
        return hash((Column, self.name))

    def __str__(self) -> str:
        prefix = "" if self.namespace is None else str(self.namespace)
        if self.table is not None:
            prefix += "" if not prefix else "."
            if isinstance(self.table.parent, Alias):
                prefix += str(self.table.parent.name)
            else:
                prefix += str(self.table)
        prefix += "." if prefix else ""
        return prefix + str(self.name)


@dataclass(eq=False)
class Wildcard(Expression):
    """wildcard or '*' expression"""

    _table: Optional["Table"] = field(repr=False, default=None)

    @property
    def table(self) -> Optional["Table"]:
        """return the table the column was referenced from if there's one"""
        return self._table

    def add_table(self, table: "Table") -> "Wildcard":
        """add a referenced table"""
        if self._table is None:
            self._table = table
        return self

    def __hash__(self) -> int:  # pragma: no cover
        return id(Wildcard)

    def __str__(self) -> str:
        return "*"


@dataclass(eq=False)
class Table(Named):
    """a type for tables"""

    _columns: List[Column] = field(repr=False, default_factory=list)

    @property
    def columns(self) -> List[Column]:
        """return the columns referenced from this table"""
        return self._columns

    def add_columns(self, *columns: Column) -> "Table":
        """add columns referenced from this table"""
        for column in columns:
            self._columns.append(column)
            column.add_table(self)
        return self

    def __hash__(self) -> int:
        return hash((Table, self.name))

    def __str__(self) -> str:
        namespace_str = ""
        if self.namespace:
            namespace_str = str(self.namespace) + "."
        return namespace_str + str(self.name)


# pylint: disable=C0103
class JoinKind(DJEnum):
    """the accepted kinds of joins"""

    Inner = "INNER JOIN"
    LeftOuter = "LEFT JOIN"
    RightOuter = "RIGHT JOIN"
    FullOuter = "FULL JOIN"
    CrossJoin = "CROSS JOIN"


# pylint: enable=C0103
TableExpression = Union[Table, Alias[Table], "Select", Alias["Select"]]


@dataclass(eq=False)
class Join(Node):
    """a join between tables"""

    kind: JoinKind
    table: TableExpression
    on: Expression  # pylint: disable=C0103

    def __hash__(self) -> int:
        return hash((Join, self.kind))

    def __str__(self) -> str:
        return f"""{self.kind.value} {self.table}
        ON {self.on}"""


@dataclass(eq=False)
class From(Node):
    """a from that belongs to a select"""

    tables: List[TableExpression]
    joins: List[Join] = field(default_factory=list)

    def __hash__(self) -> int:
        return id(self)

    def __str__(self) -> str:
        return (
            f"FROM {', '.join(str(table) for table in self.tables)}"
            + "\n"
            + "\n".join(str(join) for join in self.joins)
        )


@dataclass(eq=False)
class Select(Expression):
    """a single select statement type"""

    from_: From
    group_by: List[Expression] = field(default_factory=list)
    having: Optional[Expression] = None
    projection: List[Expression] = field(default_factory=list)
    where: Optional[Expression] = None
    limit: Optional[Number] = None
    distinct: bool = False

    def __hash__(self) -> int:
        return id(self)

    def __str__(self) -> str:
        parts = ["SELECT "]
        if self.distinct:
            parts.append("DISTINCT ")
        projection = ",\n\t".join(str(exp) for exp in self.projection)
        parts.extend((projection, "\n", str(self.from_), "\n"))
        if self.where is not None:
            parts.extend(("WHERE ", str(self.where), "\n"))
        if self.group_by:
            parts.extend(("GROUP BY ", ", ".join(str(exp) for exp in self.group_by)))
        if self.having is not None:
            parts.extend(("HAVING ", str(self.having), "\n"))
        if self.limit is not None:
            parts.extend(("LIMIT ", str(self.limit), "\n"))
        return " ".join(parts)


@dataclass(eq=False)
class Query(Expression):
    """overarching query type"""

    select: "Select"
    ctes: List[Alias["Select"]] = field(default_factory=list)

    def __hash__(self):
        return id(self)

    def __str__(self) -> str:
        subquery = bool(self.parent)
        ctes = ",\n".join(f"{cte.name} AS ({(cte.child)})" for cte in self.ctes)
        with_ = "WITH" if ctes else ""
        select = f"({(self.select)})" if subquery else (self.select)
        return f"""
            {with_}
            {ctes}
            {select}
        """.strip()
