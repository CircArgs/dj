"""
Utils for parsing partial sql strings to ast nodes
"""

from typing import Optional
from dj.sql.parsing import ast, parse


def parse_column_expression(
    expression: str, dialect: Optional[str] = None
) -> ast.Expression:
    """
    Parses a string of a sql expression into the DJ ast form
    """
    query = f"SELECT {expression}"
    tree = parse(query, dialect=dialect)
    return tree.select.projection[0]


def parse_table_expression(
    expression: str, dialect: Optional[str] = None
) -> ast.TableExpression:
    """
    Parses a string of a sql table expression into the DJ ast form
    """
    query = f"SELECT * FROM {expression}"
    tree = parse(query, dialect=dialect)
    return tree.select.from_.tables[0]
