"""Functions to add to an ast DJ node queries"""

from functools import reduce
from string import ascii_letters, digits
from typing import Dict, List, Optional, Tuple

from sqlmodel import Session

from dj.construction.build_planning import (
    BuildPlan,
    generate_build_plan,
    optimize_level_by_cost,
    optimize_level_by_database_id,
)
from dj.models.column import Column
from dj.models.database import Database
from dj.models.node import Node, NodeType
from dj.sql.parsing import ast

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
    "/": "FSLSH",
    "\\": "BSLSH",
    "|": "PIPE",
}


def amenable_name(name: str) -> str:
    """Takes a string and makes it have only alphanumerics"""
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
    build_plan: BuildPlan,
    build_plan_depth: int,
    database: Database,
    dialect: Optional[str] = None,
) -> ast.Select:
    """transforms a select ast by replacing dj node references with their asts"""

    _, build_plan_lkp = build_plan

    dimension_columns: Dict[Node, List[ast.Column]] = {}
    tables: Dict[Node, List[ast.Table]] = {}

    for table in select.find_all(ast.Table):
        if node := table.dj_node:
            tables[node] = tables.get(node) or []
            tables[node].append(table)

    for col in select.find_all(ast.Column):
        if isinstance(col.table, ast.Table):
            if node := col.table.dj_node:
                if node.type == NodeType.DIMENSION:
                    dimension_columns[node] = dimension_columns.get(node) or []
                    dimension_columns[node].append(col)

    for dim_node, dim_cols in dimension_columns.items():
        if dim_node not in tables:  # need to join dimension
            if build_plan_depth > 0:  # continue following build plan
                alias = amenable_name(dim_node.name)
                join_info: Dict[str, Tuple[Node, List[Column]]] = {}
                for table_node in tables:
                    join_dim_cols = [
                        col for col in table_node.columns if col.dimension == dim_node
                    ]
                    join_info[table_node] = join_dim_cols

                _, dim_build_plan = build_plan_lkp[dim_node]
                dim_ast, _ = dim_build_plan
                dim_query: ast.Query = build_query(
                    session,
                    dim_ast,
                    dim_build_plan,
                    build_plan_depth - 1,
                    database,
                    dialect,
                )

                dim_select = dim_query.select
                dim_ast = ast.Alias(ast.Name(alias), child=dim_select)
            else:
                dim_table = [
                    table
                    for table in dim_node.tables
                    if table.database.id == database.id
                ][0]
                dim_ast = ast.Table(
                    ast.Name(dim_table.table),
                    namespace=ast.Namespace(
                        [
                            ast.Name(s)
                            for s in (dim_table.catalog, dim_table.schema_)
                            if s
                        ],
                    ),
                )

            for dim_col in dim_cols:
                dim_col.add_table(dim_ast)

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
                                    ast.Name(col.dimension_column),
                                    _table=dim_ast,
                                ),
                            ),
                        )
                joins.append(
                    ast.Join(
                        ast.JoinKind.LeftOuter,
                        dim_ast,
                        reduce(
                            lambda l, r: ast.BinaryOp(ast.BinaryOpKind.And, l, r),
                            on,
                        ),
                    ),
                )

            select.from_.joins += joins
    for node, tbls in tables.items():

        if build_plan_depth > 0:  # continue following build plan
            _, node_build_plan = build_plan_lkp[node]
            node_ast, _ = node_build_plan
            node_query = build_query(
                session,
                node_ast,
                node_build_plan,
                build_plan_depth - 1,
                database,
                dialect,
            )
            alias = amenable_name(node.name)
            node_select = node_query.select
            node_ast = ast.Alias(ast.Name(alias), child=node_select)
            for tbl in tbls:
                select.replace(tbl, node_ast)
        else:
            node_table = [
                table for table in node.tables if table.database.id == database.id
            ][0]
            node_ast = ast.Table(
                ast.Name(node_table.table),
                namespace=ast.Namespace(
                    [
                        ast.Name(s)
                        for s in (node_table.catalog, node_table.schema_)
                        if s
                    ],
                ),
            )

        for tbl in tbls:
            select.replace(tbl, node_ast)

    return select


def build_query(
    session: Session,
    query: ast.Query,
    build_plan: BuildPlan,
    build_plan_depth: int,
    database: Database,
    dialect: Optional[str] = None,
) -> ast.Query:
    """transforms a query ast by replacing dj node references with their asts"""
    select = query.to_select()
    build_select(session, select, build_plan, build_plan_depth, database, dialect)
    for i, exp in enumerate(select.projection):
        if not isinstance(exp, ast.Named):
            name = f"_col{i}"
            aliased = ast.Alias(ast.Name(name), child=exp)
            # only replace those that are identical in memory
            select.replace(exp, aliased, lambda a, b: id(a) == id(b))
    return query


async def build_node(
    session: Session,
    node: Node,
    dialect: Optional[str] = None,
    database_id: Optional[int] = None,
) -> ast.Query:
    """transforms a query ast by replacing dj node references with their asts"""
    build_plan = generate_build_plan(session, node, dialect)
    if database_id is not None:
        build_plan_depth, database = await optimize_level_by_database_id(
            build_plan,
            database_id,
        )
    else:
        build_plan_depth, database = await optimize_level_by_cost(build_plan)

    query = build_plan[0]
    return (
        build_query(session, query, build_plan, build_plan_depth, database, dialect),
        database,
    )
