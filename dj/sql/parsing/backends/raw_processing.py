"""tools to facilitate processing raw selections of queries"""

import regex as re
from typing import Tuple, Dict, Optional, List

from sqlmodel import col
from dj.construction.utils import amenable_name
from dj.sql.parsing.ast import Raw, Column, Name, Namespace
from dj.sql.parsing.backends.exceptions import DJParseException
from dj.models.column import ColumnType

raw_pattern = re.compile(r"\${(?P<expr>.*?)\s*?:\s*?(?P<type>.*?)}")
col_pattern = re.compile(r"{\s*?(?P<expr>.*?)\s*?}")

def clean_hash(string: str)->str:
    dirty = hash(string)
    if dirty<0:
        return f"N{abs(dirty)}"
    return str(dirty)

def process_raw(query: str, dialect: Optional[str] = None) -> Tuple[str, List[Raw]]:
    """processes raw parts of a query for addition to the ast
    without raw preprocessing a query can be unparseable
    """

    from dj.sql.parsing.backends.sqloxide import parse

    raws = raw_pattern.finditer(query)

    raw_nodes = []
    for raw in raws:
        expr, type_name = raw.group("expr"), raw.group("type")
        type = ColumnType[type_name.strip().upper()]
        inner_expressions = col_pattern.finditer(expr)
        col_exprs = []
        col_exprs_hashes = []
        new_expr = expr[:]
        for inner in inner_expressions:
            col_exprs.append(inner.group("expr"))
            col_exprs_hash = f"EXPR_{clean_hash(col_exprs[-1])}"
            col_exprs_hashes.append(col_exprs_hash)
            start, end = inner.span()
            new_expr = new_expr[:start] + "{" + col_exprs_hash + "}" + new_expr[end:]

        cols = parse(f"SELECT {', '.join(col_exprs)}", dialect).select.projection
        raw_name = f"RAW_{clean_hash(expr)}"
        start, end = raw.span()
        query = query[:start] + raw_name + query[end:]
        raw_nodes.append(Raw(raw_name, new_expr, type, cols, col_exprs_hashes))

    return query, raw_nodes
