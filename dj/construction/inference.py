"""
Functions for type inference.
"""

# pylint: disable=unused-argument

from functools import singledispatch

from dj.sql.functions import function_registry
from dj.sql.parsing import ast
from dj.sql.parsing.backends.exceptions import DJParseException
from dj.typing import ColumnType


@singledispatch
def get_type_of_expression(expression: ast.Expression) -> ColumnType:
    raise NotImplementedError(f"Cannot get type of expression {expression}")


@get_type_of_expression.register
def _(expression: ast.Alias):
    return get_type_of_expression(expression.child)


@get_type_of_expression.register
def _(expression: ast.Column):
    # column has already determined/stated its type
    if expression.type:
        return expression.type

    # column was derived from some other expression we can get the type of
    if expression.expression:
        return get_type_of_expression(expression.expression)

    # column is from a table expression we can look through
    if table_pos_alias := expression.table:
        if isinstance(table, ast.Alias):
            table = table_pos_alias.child
        else:
            table = table_pos_alias
        if isinstance(table, ast.Table):
            if table.dj_node:
                for col in table.dj_node.columns:
                    if col.name == expression.name.name:
                        expression.set_type(col.type)
                        return col.type
            else:
                raise DJParseException(
                    f"Cannot resolve type of column {expression}. "
                    "column's table does not have a DJ Node."
                )
        else:
            raise DJParseException(
                f"Cannot resolve type of column {expression}. "
                "DJ does not currently traverse subqueries for type information. "
                "Consider extraction first."
            )
        # else:#if subquery
        # currently don't even bother checking subqueries.
        # the extract will have built it for us in crucial cases
    raise DJParseException(f"Cannot resolve type of column {expression}.")


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
def _(expression: ast.Wildcard):
    return ColumnType.WILDCARD


@get_type_of_expression.register
def _(expression: ast.Function):
    name = expression.name.name.upper()
    dj_func = function_registry[name]
    return dj_func.infer_type(*(get_type_of_expression(exp) for exp in expression.args))
