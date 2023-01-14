"""Functions to add to an ast DJ node queries"""

from dataclasses import dataclass, field
from itertools import chain
from functools import reduce
from typing import Dict, Generator, Iterable, List, Optional, Set, Tuple, Union, cast

from sqlmodel import Session

from dj.errors import DJError, DJException, ErrorCode
from dj.models.node import Node, NodeType
from dj.models.column import Column
from dj.models.database import Database
from dj.sql.parsing import ast
from dj.sql.parsing.backends.sqloxide import parse
from dj.construction.compile import compile_query
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
    select: ast.Select,
    dialect: Optional[str] = None,
    database: Optional[Database] = None
) -> ast.Select:
    """transforms a select ast by replacing dj node references with their asts"""
    dimension_columns: Dict[Node, List[ast.Column]] = {}
    tables: Dict[Node, List[ast.Table]] = {}

    for table in select.find_all(ast.Table):
        if node := table.dj_node:
            if node.type!=NodeType.SOURCE:
                tables[node] = tables.get(node) or []
                tables[node].append(table)
        else:
            raise Exception(f"To build, Table {table} requires a pointer to a DJ Node.")

    for col in select.find_all(ast.Column):
        if isinstance(col.table, ast.Table):
            if node := col.table.dj_node:
                if node.type == NodeType.DIMENSION:
                    dimension_columns[node] = dimension_columns.get(node) or []
                    dimension_columns[node].append(col)

    for dim_node, dim_cols in dimension_columns.items():
        if dim_node not in tables:  # need to join dimension
            alias = amenable_name(dim_node.name)
            join_info: Dict[str, Tuple[Node, List[Column]]] = {}
            for table_node in tables:
                join_dim_cols = [
                    col for col in table_node.columns if col.dimension == dim_node
                ]
                join_info[table_node] = join_dim_cols
            dim_query = build_node(session, dim_node, dialect)

            if dim_query.ctes:  # will have to build ctes in as subqueries to the select
                raise Exception("DJ does not currently support ctes here.")

            dim_select = dim_query.select
            dim_ast = ast.Alias(ast.Name(alias), child=dim_select)
            for dim_col in dim_cols:
                dim_col.add_table(dim_select)

            joins: List[ast.Join] = []

            for table_node, cols in join_info.items():
                ast_tables = tables[table_node]
                for table in ast_tables:
                    on = []
                    for col in cols:
                        on.append(
                            ast.BinaryOp(
                                ast.BinaryOpKind.Eq,
                                ast.Column(ast.Name(col.name), _table=table),
                                ast.Column(
                                    ast.Name(col.dimension_column), _table=dim_ast
                                ),
                            ),
                        )
                joins.append(
                    ast.Join(
                        ast.JoinKind.LeftOuter,
                        dim_ast,
                        reduce(
                            lambda l, r: ast.BinaryOp(ast.BinaryOpKind.And, l, r), on
                        ),
                    ),
                )

            select.from_.joins += joins

    for node, tbls in tables.items():
        node_query = build_node(session, node, dialect)

        if (
            node_query.ctes
        ):  # will have to build ctes in as subqueries to the select
            raise Exception("DJ does not currently support ctes here.")

        node_select = node_query.select
        node_ast = ast.Alias(ast.Name(alias), child=node_select)
        for tbl in tbls:
            select.replace(tbl, node_ast)


    #sources
    sources: Dict[Node, List[ast.Table]] = {}

    for table in select.find_all(ast.Table):
        if node := table.dj_node:
            if node.type==NodeType.SOURCE:
                tables[node] = tables.get(node) or []
                tables[node].append(table)
        else:
            raise Exception(f"To build, Table {table} requires a pointer to a DJ Node.")

    source_dbs_intersect = []
    source_db_costs = {}
    for node, tbls in sources.items():
        db_names = set()
        for db_table in node.tables:
            name = db_table.table
            source_db_costs[name] = source_db_costs.get(name, 0) + db_table.cost
            db_names.add(name)
        source_dbs_intersect.append(db_names)

    source_intersect = reduce(lambda a, b: a&b, source_dbs_intersect)

    if not source_intersect:
        raise Exception("Sources do not share a common database.")
    return select


def build_query(
    session: Session,
    query: ast.Query,
    dialect: Optional[str] = None,
    database: Optional[Database] = None
) -> ast.Query:
    """transforms a query ast by replacing dj node references with their asts"""
    # query = query.copy()
    select = query.to_select()

    build_select(session, select, dialect)
    for i, exp in enumerate(select.projection):
        if not isinstance(exp, ast.Named):
            name = f"_col{i}"
            aliased = ast.Alias(ast.Name(name), child=exp)
            select.replace(exp, aliased)
    return query


def build_node(
    session: Session,
    node: Node,
    dialect: Optional[str] = None,
    database: Optional[Database] = None
) -> ast.Query:
    """transforms a query ast by replacing dj node references with their asts"""
    query = parse(node.query, dialect)
    query = compile_query(session, query)
    return build_query(session, query, dialect)
