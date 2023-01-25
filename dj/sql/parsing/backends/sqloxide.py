"""
parsing backend turning sqloxide output into DJ AST
"""
from typing import List, Optional, Set, Union

from sqloxide import parse_sql

from dj.sql.parsing.ast import (
    Alias,
    Between,
    BinaryOp,
    BinaryOpKind,
    Boolean,
    Case,
    Column,
    Expression,
    From,
    Function,
    In,
    IsNull,
    Join,
    JoinKind,
    Name,
    Namespace,
    Number,
    Operation,
    Over,
    Order,
    Query,
    Select,
    String,
    Table,
    TableExpression,
    UnaryOp,
    UnaryOpKind,
    Value,
    Wildcard,
)
from dj.sql.parsing.backends.exceptions import DJParseException
from dj.sql.parsing.backends.raw_processing import process_raw


def match_keys(parse_tree: dict, *keys: Set[str]) -> Optional[Set[str]]:
    """match a parse tree having exact keys"""
    tree_keys = set(parse_tree.keys())
    for key in keys:
        if key == tree_keys:
            return key


def match_keys_subset(parse_tree: dict, *keys: Set[str]) -> Optional[Set[str]]:
    """match a parse tree having a subset of keys"""
    tree_keys = set(parse_tree.keys())
    for key in keys:
        if key <= tree_keys:
            return key


def parse_op(parse_tree: dict) -> Operation:
    """parse an unary or binary operation"""
    if match_keys(parse_tree, {"BinaryOp"}):
        subtree = parse_tree["BinaryOp"]
        for exp in BinaryOpKind:
            binop_kind = exp.name
            if subtree["op"] == binop_kind:
                return BinaryOp(
                    BinaryOpKind[binop_kind],
                    parse_expression(subtree["left"]),
                    parse_expression(subtree["right"]),
                )
        raise DJParseException(f"Unknown operator {subtree['op']}")  # pragma: no cover
    if match_keys(parse_tree, {"UnaryOp"}):
        subtree = parse_tree["UnaryOp"]
        for exp in UnaryOpKind:  # type: ignore
            uniop_kind = exp.name
            if subtree["op"] == uniop_kind:
                return UnaryOp(
                    UnaryOpKind[uniop_kind],
                    parse_expression(subtree["expr"]),
                )
        raise DJParseException(f"Unknown operator {subtree['op']}")  # pragma: no cover
    if match_keys(parse_tree, {"Between"}):
        subtree = parse_tree["Between"]
        between = Between(
            parse_expression(subtree["expr"]),
            parse_expression(subtree["low"]),
            parse_expression(subtree["high"]),
        )
        if subtree["negated"]:
            return UnaryOp(UnaryOpKind.Not, between)
        return between

    raise DJParseException("Failed to parse Operator")  # pragma: no cover


def parse_case(parse_tree: dict) -> Case:
    """parse a case expressions"""
    if match_keys(parse_tree, {"conditions", "else_result", "operand", "results"}):
        return Case(
            [parse_expression(exp) for exp in parse_tree["conditions"]],
            parse_expression(parse_tree["else_result"])
            if parse_tree["else_result"] is not None
            else None,
            parse_expression(parse_tree["operand"])
            if parse_tree["operand"] is not None
            else None,
            [parse_expression(exp) for exp in parse_tree["results"]],
        )
    raise DJParseException("Failed to parse Case")  # pragma: no cover


def parse_expression(  # pylint: disable=R0911,R0912
    parse_tree: Union[dict, str],
) -> Expression:
    """parse an expression"""
    if isinstance(parse_tree, str):
        if parse_tree == "Wildcard":
            return Wildcard()
    else:
        if match_keys(parse_tree, {"Value"}):
            return parse_value(parse_tree["Value"])
        if match_keys(parse_tree, {"Wildcard"}):
            return parse_expression("Wildcard")
        if match := match_keys(parse_tree, {"InList"}, {"InSubquery"}):
            return parse_in(parse_tree[match.pop()])
        if match_keys(parse_tree, {"Nested"}):
            return parse_expression(parse_tree["Nested"])
        if match_keys(parse_tree, {"UnaryOp"}, {"BinaryOp"}, {"Between"}):
            return parse_op(parse_tree)
        if match_keys(parse_tree, {"Unnamed"}):
            return parse_expression(parse_tree["Unnamed"])
        if match_keys(parse_tree, {"UnnamedExpr"}):
            return parse_expression(parse_tree["UnnamedExpr"])
        if match_keys(parse_tree, {"Expr"}):
            return parse_expression(parse_tree["Expr"])
        if match_keys(parse_tree, {"Case"}):
            return parse_case(parse_tree["Case"])
        if match_keys(parse_tree, {"Function"}):
            return parse_function(parse_tree["Function"])
        if match_keys(parse_tree, {"IsNull"}, {"IsNotNull"}):
            if "IsNull" in parse_tree:
                return IsNull(parse_expression(parse_tree["IsNull"]))
            return UnaryOp(
                UnaryOpKind.Not,
                IsNull(
                    parse_expression(parse_tree["IsNotNull"]),
                ),
            )
        if match_keys(parse_tree, {"Identifier"}, {"CompoundIdentifier"}):
            return parse_column(parse_tree)
        if match_keys(parse_tree, {"ExprWithAlias"}):
            subtree = parse_tree["ExprWithAlias"]
            return Alias(
                parse_name(subtree["alias"]),
                child=parse_column(subtree["expr"]),
            )
        if match_keys(parse_tree, {"Subquery"}):
            subquery = parse_query(parse_tree["Subquery"])
            return subquery.to_select()
    raise DJParseException("Failed to parse Expression")  # pragma: no cover


def parse_value(parse_tree: dict) -> Value:
    """parse a primitive value"""
    if match_keys(parse_tree, {"Value"}):
        return parse_value(parse_tree["Value"])
    if match_keys(parse_tree, {"Number"}):
        return Number(parse_tree["Number"][0])
    if match_keys(parse_tree, {"SingleQuotedString"}):
        return String(parse_tree["SingleQuotedString"])
    if match_keys(parse_tree, {"Boolean"}):
        return Boolean(parse_tree["Boolean"])
    raise DJParseException("Not a primitive")  # pragma: no cover


def parse_namespace(parse_tree: List[dict]) -> Namespace:
    """parse a namespace"""
    return Namespace([parse_name(name) for name in parse_tree])


def parse_name(parse_tree: dict) -> Name:
    """parse a name"""
    if match_keys(parse_tree, {"value", "quote_style"}):
        return Name(
            name=parse_tree["value"],
            quote_style=parse_tree["quote_style"]
            if parse_tree["quote_style"] is not None
            else "",
        )
    raise DJParseException("Failed to parse Name")  # pragma: no cover


def parse_column(parse_tree: dict):
    """parse a column"""
    if match_keys(parse_tree, {"Identifier"}, {"CompoundIdentifier"}):
        if "CompoundIdentifier" in parse_tree:
            subtree = parse_tree["CompoundIdentifier"]
            return parse_namespace(subtree).to_named_type(Column)
        return parse_name(parse_tree["Identifier"]).to_named_type(Column)
    return parse_expression(parse_tree)


def parse_table(parse_tree: dict) -> TableExpression:
    """parse a table"""
    if match_keys(parse_tree, {"Derived"}):
        subtree = parse_tree["Derived"]
        if subtree["lateral"]:
            raise DJParseException("Parsing does not support lateral subqueries")

        alias = subtree["alias"]
        subquery = parse_query(subtree["subquery"])
        if subquery.ctes:
            raise DJParseException("CTEs are not allowed in a subquery")
        subselect = subquery.select
        if alias:
            if alias["columns"]:
                raise DJParseException(  # pragma: no cover
                    "Parsing does not support columns in derived from.",
                )
            aliased: Alias[Select] = Alias(
                parse_name(alias["name"]),
                child=subselect,
            )
            return aliased
        return subselect
    if match_keys(parse_tree, {"Table"}):
        subtree = parse_tree["Table"]

        table = parse_namespace(subtree["name"]).to_named_type(Table)
        if subtree["alias"]:
            aliased: Alias[Table] = Alias(  # type: ignore
                parse_name(subtree["alias"]["name"]),
                child=table,
            )
            return aliased
        return table

    raise DJParseException("Failed to parse Table")  # pragma: no cover


def parse_in(parse_tree: dict) -> In:
    """parse an in statement"""
    if match_keys(parse_tree, {"expr", "list", "negated"}):
        source = [parse_expression(expr) for expr in parse_tree["list"]]
        return In(parse_expression(parse_tree["expr"]), source, parse_tree["negated"])
    if match_keys(parse_tree, {"expr", "subquery", "negated"}):
        subquery = parse_tree["subquery"]
        source = parse_query(subquery).to_select()
        return In(parse_expression(parse_tree["expr"]), source, parse_tree["negated"])
    raise DJParseException("Failed to parse IN")  # pragma: no cover


def parse_over(parse_tree: dict) -> Over:
    """parse the over of a function"""
    if match_keys(parse_tree, {"partition_by", "order_by", "window_frame"}):
        if parse_tree["window_frame"] is not None:
            raise DJParseException("window frames are not supported.")
        partition_by = [parse_expression(exp) for exp in parse_tree["partition_by"]]
        order_by = [parse_order(exp) for exp in parse_tree["order_by"]]
        return Over(partition_by, order_by)
    raise DJParseException("Failed to parse OVER")  # pragma: no cover


def parse_order(parse_tree: dict) -> Order:
    """parse the order parts of an order by or window function"""
    if match_keys(parse_tree, {"expr", "asc", "nulls_first"}):
        if parse_tree["nulls_first"] is not None:
            raise DJParseException("nulls first is not supported.")
        return Order(
            expr=parse_expression(parse_tree["expr"]),
            asc=True if parse_tree["asc"] else False,
        )
    raise DJParseException("Failed to parse ORDER BY expression.")  # pragma: no cover


def parse_function(parse_tree: dict) -> Function:
    """parse a function operating on an expression"""
    if match_keys_subset(parse_tree, {"name", "args", "over", "distinct"}):
        args = parse_tree["args"]
        names = parse_tree["name"]
        namespace, name = parse_namespace(names).pop_self()
        over = parse_tree["over"] and parse_over(parse_tree["over"])
        return Function(
            name,
            args=[parse_expression(exp) for exp in args],
            distinct=parse_tree["distinct"],
            over=over,
        ).add_namespace(namespace)
    raise DJParseException("Failed to parse Function")  # pragma: no cover


def parse_join(parse_tree: dict) -> Join:
    """parse a join of a select"""
    if match_keys(
        parse_tree,
        {"relation", "join_operator"},
    ):
        relation = parse_tree["relation"]
        join_operator = parse_tree["join_operator"]
        for exp in JoinKind:
            join_kind = exp.name
            if match_keys(
                join_operator,
                {join_kind},
            ):
                if "On" not in join_operator[join_kind]:
                    raise DJParseException("Join must specify ON")
                return Join(
                    JoinKind[join_kind],
                    parse_table(relation),
                    parse_expression(join_operator[join_kind]["On"]),
                )

    raise DJParseException("Failed to parse Join")  # pragma: no cover


def parse_from(parse_list: List[dict]) -> From:
    """parse the from of a select"""
    tables, joins = [], []
    for parse_tree in parse_list:
        if match_keys(
            parse_tree,
            {"relation", "joins"},
        ):
            tables.append(parse_table(parse_tree["relation"]))
            joins += [parse_join(join) for join in parse_tree["joins"]]
        else:
            raise DJParseException("Failed to parse From")  # pragma: no cover
    return From(tables, joins)


def parse_select(parse_tree: dict) -> Select:
    """parse the select of a query or subquery"""
    if match_keys_subset(
        parse_tree,
        {"distinct", "from", "group_by", "having", "projection", "selection"},
    ):
        return Select(
            parse_from(parse_tree["from"]),
            [parse_expression(exp) for exp in parse_tree["group_by"]],
            parse_expression(parse_tree["having"])
            if parse_tree["having"] is not None
            else None,
            [parse_expression(exp) for exp in parse_tree["projection"]],
            parse_expression(parse_tree["selection"])
            if parse_tree["selection"] is not None
            else None,
            None,
            parse_tree["distinct"],
        )

    raise DJParseException("Failed to parse Select")  # pragma: no cover


def parse_ctes(parse_tree: dict) -> List[Alias[Select]]:
    """parse the ctes of a query"""
    if match_keys_subset(parse_tree, {"cte_tables"}):
        subtree = parse_tree["cte_tables"]
        ctes: List[Alias[Select]] = []
        for aliased_query in subtree:
            ctes.append(
                Alias(
                    parse_name(aliased_query["alias"]["name"]),
                    child=parse_select(aliased_query["query"]["body"]["Select"]),
                ),
            )
        return ctes
    raise DJParseException("Failed to parse ctes")  # pragma: no cover


def parse_query(parse_tree: dict) -> Query:
    """parse a query (ctes+select) statement"""
    if match_keys_subset(parse_tree, {"with", "body", "limit"}):
        body = parse_tree["body"]
        if match_keys(body, {"Select"}):
            select = parse_select(body["Select"])
            select.limit = None
            if parse_tree["limit"] is not None:
                limit_value = parse_value(parse_tree["limit"])
                select.limit = limit_value  # type: ignore
            if parse_tree["order_by"] is not None:
                order_by = [parse_order(exp) for exp in parse_tree["order_by"]]
                select.order_by = order_by
            return Query(
                ctes=parse_ctes(parse_tree["with"])
                if parse_tree["with"] is not None
                else [],
                select=select,
            )

    raise DJParseException("Failed to parse query")  # pragma: no cover


def parse_oxide_tree(parse_tree: dict) -> Query:
    """take a sqloxide parsed statement ast dict and transform it into a DJ ast"""
    if match_keys(parse_tree, {"Query"}):
        return parse_query(
            parse_tree["Query"],
        )

    raise DJParseException("Failed to parse Query")  # pragma: no cover


def parse(sql: str, dialect: Optional[str] = None) -> Query:
    """Parse a string into a DJ ast using sqloxide backend.

    Parses only a single Select query (can include ctes)

    """
    if dialect is None:
        dialect = "ansi"
    sql, raws = process_raw(sql, dialect)
    oxide_parsed = parse_sql(sql, dialect)
    if len(oxide_parsed) != 1:
        raise DJParseException("Expected a single sql statement.")
    ast = parse_oxide_tree(oxide_parsed[0])
    for raw in raws:
        for col in ast.filter(
            lambda node: isinstance(node, Column) and node.name.name == raw.name
        ):
            ast.replace(col, raw)
    return ast
