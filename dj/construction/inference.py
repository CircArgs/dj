"""
Functions for type inference.
"""

# pylint: disable=unused-argument

from functools import singledispatch
from typing import Callable, Dict

from dj.sql.functions import function_registry
from dj.sql.parsing import ast
from dj.sql.parsing.backends.exceptions import DJParseException
from dj.typing import ColumnType


@singledispatch
def get_type_of_expression(expression: ast.Expression) -> ColumnType:
    """
    Get the type of an expression
    """
    raise NotImplementedError(f"Cannot get type of expression {expression}")


@get_type_of_expression.register
def _(expression: ast.Alias):
    return get_type_of_expression(expression.child)


@get_type_of_expression.register
def _(expression: ast.Column):
    # column has already determined/stated its type
    if expression._type:  # pylint: disable=W0212
        return expression._type  # pylint: disable=W0212

    # column was derived from some other expression we can get the type of
    if expression.expression:
        type_ = get_type_of_expression(expression.expression)
        expression.add_type(type_)
        return type_

    # column is from a table expression we can look through
    if table_or_alias := expression.table:
        if isinstance(table_or_alias, ast.Alias):
            table = table_or_alias.child
        else:
            table = table_or_alias
        if isinstance(table, ast.Table):
            if table.dj_node:
                for col in table.dj_node.columns:  # pragma: no cover
                    if col.name == expression.name.name:
                        expression.add_type(col.type)
                        return col.type
            else:
                raise DJParseException(
                    f"Cannot resolve type of column {expression}. "
                    "column's table does not have a DJ Node.",
                )
        else:
            raise DJParseException(
                f"Cannot resolve type of column {expression}. "
                "DJ does not currently traverse subqueries for type information. "
                "Consider extraction first.",
            )
        # else:#if subquery
        # currently don't even bother checking subqueries.
        # the extract will have built it for us in crucial cases
    raise DJParseException(f"Cannot resolve type of column {expression}.")


@get_type_of_expression.register
def _(expression: ast.Null):
    return ColumnType.NULL


@get_type_of_expression.register
def _(expression: ast.String):
    return ColumnType.STR


@get_type_of_expression.register
def _(expression: ast.Number):
    if isinstance(expression.value, int):
        return ColumnType.INT
    return ColumnType.FLOAT


@get_type_of_expression.register
def _(expression: ast.Boolean):
    return ColumnType.BOOL


@get_type_of_expression.register
def _(expression: ast.Wildcard):  # pragma: no cover
    return ColumnType.WILDCARD


@get_type_of_expression.register
def _(expression: ast.Function):  # pragma: no cover
    name = expression.name.name.upper()
    dj_func = function_registry[name]
    return dj_func.infer_type_from_types(
        *(get_type_of_expression(exp) for exp in expression.args)
    )


@get_type_of_expression.register
def _(expression: ast.Raw):
    return expression.type_


@get_type_of_expression.register
def _(expression: ast.Cast):
    return expression.type_


@get_type_of_expression.register
def _(expression: ast.IsNull):
    return ColumnType.BOOL


@get_type_of_expression.register
def _(expression: ast.In):
    return ColumnType.BOOL


@get_type_of_expression.register
def _(expression: ast.Select):
    if len(expression.projection) != 1:
        raise DJParseException(
            "Can only infer type of a SELECT when it "
            f"has a single expression in its projection. In {expression}.",
        )
    return get_type_of_expression(expression.projection[0])


@get_type_of_expression.register
def _(expression: ast.Between):
    expr_type = get_type_of_expression(expression.expr)
    low_type = get_type_of_expression(expression.low)
    high_type = get_type_of_expression(expression.high)
    if expr_type == low_type == high_type:
        return ColumnType.BOOL
    raise DJParseException(
        f"BETWEEN expects all elements to have the same type got "
        f"{expr_type} BETWEEN {low_type} AND {high_type} in {expression}.",
    )


@get_type_of_expression.register
def _(expression: ast.UnaryOp):
    kind = expression.op
    type_ = get_type_of_expression(expression.expr)

    def raise_unop_exception():
        raise DJParseException(
            "Incompatible type in unary operation "
            f"{expression}. Got {type} in {expression}.",
        )

    UNOP_TYPE_COMBO_LOOKUP: Dict[  # pylint: disable=C0103
        ast.UnaryOpKind,
        Callable[[ColumnType], ColumnType],
    ] = {
        ast.UnaryOpKind.Not: lambda type: ColumnType.BOOL
        if type == ColumnType.BOOL
        else raise_unop_exception(),
        ast.UnaryOpKind.Minus: lambda type: type_
        if type in (ColumnType.INT, ColumnType.FLOAT)
        else raise_unop_exception(),
        ast.UnaryOpKind.Plus: lambda type: type_
        if type_ in (ColumnType.INT, ColumnType.FLOAT)
        else raise_unop_exception(),
    }
    return UNOP_TYPE_COMBO_LOOKUP[kind](type_)


@get_type_of_expression.register
def _(expression: ast.BinaryOp):
    kind = expression.op
    left_type = get_type_of_expression(expression.left)
    right_type = get_type_of_expression(expression.right)

    def raise_binop_exception():
        raise DJParseException(
            "Incompatible types in binary operation "
            f"{expression}. Got left {left_type}, right {right_type}.",
        )

    BINOP_TYPE_COMBO_LOOKUP: Dict[  # pylint: disable=C0103
        ast.BinaryOpKind,
        Callable[[ColumnType, ColumnType], ColumnType],
    ] = {
        ast.BinaryOpKind.And: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.Or: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.Is: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.Eq: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.NotEq: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.Gt: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.Lt: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.GtEq: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.LtEq: lambda left, right: ColumnType.BOOL,
        ast.BinaryOpKind.BitwiseOr: lambda left, right: ColumnType.INT
        if left == right == ColumnType.INT
        else raise_binop_exception(),
        ast.BinaryOpKind.BitwiseAnd: lambda left, right: ColumnType.INT
        if left == right == ColumnType.INT
        else raise_binop_exception(),
        ast.BinaryOpKind.BitwiseXor: lambda left, right: ColumnType.INT
        if left == right == ColumnType.INT
        else raise_binop_exception(),
        ast.BinaryOpKind.Multiply: lambda left, right: left
        if left == right
        else (
            ColumnType.FLOAT
            if {left, right} == {ColumnType.FLOAT, ColumnType.INT}
            else raise_binop_exception()
        ),
        ast.BinaryOpKind.Divide: lambda left, right: left
        if left == right
        else (
            ColumnType.FLOAT
            if {left, right} == {ColumnType.FLOAT, ColumnType.INT}
            else raise_binop_exception()
        ),
        ast.BinaryOpKind.Plus: lambda left, right: left
        if left == right
        else (
            ColumnType.FLOAT
            if {left, right} == {ColumnType.FLOAT, ColumnType.INT}
            else raise_binop_exception()
        ),
        ast.BinaryOpKind.Minus: lambda left, right: left
        if left == right
        else (
            ColumnType.FLOAT
            if {left, right} == {ColumnType.FLOAT, ColumnType.INT}
            else raise_binop_exception()
        ),
        ast.BinaryOpKind.Modulo: lambda left, right: ColumnType.INT
        if left == right == ColumnType.INT
        else raise_binop_exception(),
        ast.BinaryOpKind.Like: lambda left, right: ColumnType.BOOL
        if left == right == ColumnType.STR
        else raise_binop_exception(),
    }
    return BINOP_TYPE_COMBO_LOOKUP[kind](left_type, right_type)
