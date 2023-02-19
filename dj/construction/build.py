"""Functions to add to an ast DJ node queries"""
# pylint: disable=too-many-arguments,too-many-locals,too-many-nested-blocks,too-many-branches,R0401
from functools import reduce
from typing import Dict, List, Optional, Set, Tuple, cast

from sqlmodel import Session

from dj.construction.build_planning import (
    BuildPlan,
    generate_build_plan_from_query,
    optimize_level_by_cost,
    optimize_level_by_database_id,
)
from dj.construction.utils import amenable_name
from dj.errors import DJException
from dj.models.column import Column
from dj.models.database import Database
from dj.models.node import NodeRevision, NodeType
from dj.sql.parsing import ast
from dj.sql.parsing.backends.sqloxide import parse


def _get_tables_from_select(select: ast.Select) -> Dict[NodeRevision, List[ast.Table]]:
    """
    Extract all tables (source, transform, dimensions)
    """
    tables: Dict[NodeRevision, List[ast.Table]] = {}

    for table in select.find_all(ast.Table):
        if node := table.dj_node:  # pragma: no cover
            tables[node] = tables.get(node, [])
            tables[node].append(table)
    return tables


def _get_dim_cols_from_select(
    select: ast.Select,
) -> Dict[NodeRevision, List[ast.Column]]:
    """
    Extract all dimension nodes referenced as columns
    """
    dimension_columns: Dict[NodeRevision, List[ast.Column]] = {}

    for col in select.find_all(ast.Column):
        if isinstance(col.table, ast.Table):
            if node := col.table.dj_node:  # pragma: no cover
                if node.type == NodeType.DIMENSION:
                    dimension_columns[node] = dimension_columns.get(node, [])
                    dimension_columns[node].append(col)
    return dimension_columns


def _build_dimensions_on_select(
    session: Session,
    dimension_columns: Dict[NodeRevision, List[ast.Column]],
    build_plan_lookup: Dict[NodeRevision, Tuple[Set[Database], BuildPlan]],
    build_plan_depth: int,
    database: Database,
    dialect: Optional[str] = None,
):
    """
    Add all filter and agg dimensions to a select
    """

    for dim_node, dim_cols in dimension_columns.items():
        selects_map = {}
        for dim_col in dim_cols:
            select = cast(ast.Select, dim_col.get_nearest_parent_of_type(ast.Select))
            selects_map[id(select)] = select
        for select in selects_map.values():
            tables = _get_tables_from_select(select)
            if dim_node not in tables:  # need to join dimension
                join_info: Dict[NodeRevision, List[Column]] = {}
                for table_node in tables:
                    join_dim_cols = []
                    for col in table_node.columns:
                        if col.dimension and col.dimension.current == dim_node:
                            if col.dimension_column is None and not any(
                                dim_col.name == "id" for dim_col in dim_node.columns
                            ):
                                raise DJException(
                                    f"Node {table_node.node.name} specifiying dimension "
                                    f"{dim_node.node.name} on column {col.name} does not"
                                    f" specify a dimension column, but {dim_node.node.name} "
                                    f"does not have the default key `id`.",
                                )
                            join_dim_cols.append(col)

                    join_info[table_node] = join_dim_cols
                if build_plan_depth > 0:  # continue following build plan
                    alias = amenable_name(dim_node.node.name)

                    _, dim_build_plan = build_plan_lookup[dim_node]
                    dim_ast = dim_build_plan[0]
                    dim_ast.build(
                        session,
                        dim_build_plan,
                        build_plan_depth - 1,
                        database,
                        dialect,
                    )

                    dim_select = dim_ast.select
                    dim_ast = ast.Alias(
                        ast.Name(alias),
                        child=dim_select,
                    )  # type:ignore
                else:  # pragma: no cover
                    dim_table = [
                        table
                        for table in dim_node.tables
                        if table.database.id == database.id
                    ][0]
                    dim_ast = ast.Table(  # type: ignore
                        ast.Name(dim_table.table),
                        namespace=ast.Namespace(
                            [
                                ast.Name(s)
                                for s in (dim_table.catalog, dim_table.schema_)
                                if s
                            ],
                        ),
                    )

                for (
                    dim_col
                ) in dim_cols:  # replace column table references to this dimension
                    dim_col.add_table(dim_ast)  # type: ignore

                for table_node, cols in join_info.items():
                    ast_tables = tables[table_node]
                    join_on = []
                    for table in ast_tables:
                        for col in cols:
                            join_on.append(
                                ast.BinaryOp(
                                    ast.BinaryOpKind.Eq,
                                    ast.Column(ast.Name(col.name), _table=table),
                                    ast.Column(
                                        ast.Name(col.dimension_column or "id"),
                                        _table=dim_ast,  # type: ignore
                                    ),
                                ),
                            )

                    if join_on:  # table had stuff to join
                        select.from_.joins.append(  # pragma: no cover
                            ast.Join(
                                ast.JoinKind.LeftOuter,
                                dim_ast,  # type: ignore
                                reduce(
                                    lambda left, right: ast.BinaryOp(
                                        ast.BinaryOpKind.And,
                                        left,
                                        right,
                                    ),
                                    join_on,
                                ),
                            ),
                        )


def _build_tables_on_select(
    session: Session,
    select: ast.Select,
    tables: Dict[NodeRevision, List[ast.Table]],
    build_plan_lookup: Dict[NodeRevision, Tuple[Set[Database], BuildPlan]],
    build_plan_depth: int,
    database: Database,
    dialect: Optional[str] = None,
):
    """
    Add all nodes not agg or filter dimensions to the select
    """
    for node, tbls in tables.items():

        if (
            node.node.type != NodeType.SOURCE and build_plan_depth > 0
        ):  # continue following build plan
            _, node_build_plan = build_plan_lookup[node]
            node_ast = node_build_plan[0]
            node_ast.build(
                session,
                node_build_plan,
                build_plan_depth - 1,
                database,
                dialect,
            )
            alias = amenable_name(node.node.name)
            node_select = node_ast.select
            node_ast = ast.Alias(ast.Name(alias), child=node_select)  # type: ignore
            for tbl in tbls:
                select.replace(tbl, node_ast)
        else:
            node_table = [
                table for table in node.tables if table.database.id == database.id
            ][0]
            node_ast = ast.Table(  # type: ignore
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


# flake8: noqa: C901
def _build_select_ast(
    session: Session,
    select: ast.Select,
    build_plan: BuildPlan,
    build_plan_depth: int,
    database: Database,
    dialect: Optional[str] = None,
):
    """
    Transforms a select ast by replacing dj node references with their asts
    """

    _, build_plan_lookup = build_plan

    dimension_columns = _get_dim_cols_from_select(select)
    tables = _get_tables_from_select(select)

    _build_dimensions_on_select(
        session,
        dimension_columns,
        build_plan_lookup,
        build_plan_depth,
        database,
        dialect,
    )

    _build_tables_on_select(
        session,
        select,
        tables,
        build_plan_lookup,
        build_plan_depth,
        database,
        dialect,
    )


def add_filters_and_aggs_to_query_ast(
    query: ast.Query,
    dialect: Optional[str] = None,
    filters: Optional[List[str]] = None,
    dimensions: Optional[List[str]] = None,
):
    """
    Add filters and dimensions to a query ast
    """
    projection_addition = []
    if filters:
        filter_asts = (  # pylint: disable=consider-using-ternary
            query.select.where and [query.select.where] or []
        )

        for filter_ in filters:
            temp_select = parse(f"select * where {filter_}", dialect).select
            filter_asts.append(
                # use parse to get the asts from the strings we got
                temp_select.where,  # type:ignore
            )
            projection_addition += list(temp_select.find_all(ast.Column))
        query.select.where = reduce(
            lambda left, right: ast.BinaryOp(
                ast.BinaryOpKind.And,
                left,
                right,
            ),
            filter_asts,
        )

    if dimensions:
        for agg in dimensions:
            temp_select = parse(
                f"select * group by {agg}",
                dialect,
            ).select
            query.select.group_by += temp_select.group_by  # type:ignore
            projection_addition += list(temp_select.find_all(ast.Column))
    query.select.projection += [
        col.set_api_column(True).copy() for col in set(projection_addition)
    ]


async def build_node_for_database(  # pylint: disable=too-many-arguments
    session: Session,
    node: NodeRevision,
    dialect: Optional[str] = None,
    database_id: Optional[int] = None,
    filters: Optional[List[str]] = None,
    dimensions: Optional[List[str]] = None,
) -> Tuple[ast.Query, Database]:
    """
    Determines the optimal database to run the query in and builds the node appropriately
    """
    if node.query is None:
        raise Exception(
            "Node has no query. Cannot generate a build plan without a query.",
        )
    query = parse(node.query, dialect)
    top_dbs: Set[Database] = set()
    if filters or dimensions:
        add_filters_and_aggs_to_query_ast(query, dialect, filters, dimensions)
    else:  # if not dimensions then we can see if the node is directly materialized
        top_dbs = {table.database for table in node.tables}

    return await build_ast_for_database(session, query, dialect, database_id, top_dbs)


async def build_ast_for_database(  # pylint: disable=too-many-arguments
    session: Session,
    query: ast.Query,
    dialect: Optional[str] = None,
    database_id: Optional[int] = None,
    top_dbs: Optional[Set[Database]] = None,
) -> Tuple[ast.Query, Database]:
    """
    Determines the optimal database to run the query in and builds the query AST appropriately
    """
    top_dbs = top_dbs or set()
    build_plan = generate_build_plan_from_query(session, query, dialect)
    if database_id is not None:
        for top_db in top_dbs:
            if top_db.id == database_id:  # pragma: no cover
                return query, top_db

        build_plan_depth, database = await optimize_level_by_database_id(
            build_plan,
            database_id,
        )

    else:
        build_plan_depth, database = await optimize_level_by_cost(build_plan)
        for top_db in top_dbs:
            if top_db.cost <= database.cost:  # pragma: no cover
                return query, top_db

    query = build_plan[0]
    query.build(session, build_plan, build_plan_depth, database, dialect)
    return (
        query,
        database,
    )
