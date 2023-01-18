"""
tools for planning the steps a node will need to take to be built to run
"""
from functools import reduce
from typing import Dict, List, Optional, Set, Tuple

from sqlmodel import Session

from dj.construction.extract import extract_dependencies_from_node
from dj.models.database import Database
from dj.models.node import Node, NodeType
from dj.sql.dag import get_cheapest_online_database
from dj.sql.parsing import ast

BuildPlan = Tuple[ast.Query, Dict[Node, Tuple[Set[Database], "BuildPlan"]]]#type: ignore


def get_node_materialized_databases(
    node: Node,
    columns: Set[str],
) -> Set[Database]:
    """
    Return all the databases where the node is explicitly materialized
    """
    tables = [
        table
        for table in node.tables
        if columns <= {column.name for column in table.columns}
    ]
    return {table.database for table in tables}


def generate_build_plan(
    session: Session,
    node: Node,
    dialect: Optional[str] = None,
) -> BuildPlan:
    """
    creates a build plan to be followed by the building of a node

    processes nodes recursively extracting dependencies to
        build the BuildPlan which specifies an
            ast, node: {Databases, BuildPlan}
        that can be recursively followed as deep as desired to
        replace nodes with the desired ast
    """
    if node.query is None:
        raise Exception(
            "Node has no query. Cannot generate a build plan without a query.",
        )
    tree, deps, _ = extract_dependencies_from_node(session, node, dialect)
    databases = {}
    for node, tables in deps.items():
        columns = {col.name.name for table in tables for col in table.columns}

        node_mat_dbs = get_node_materialized_databases(node, columns)
        build_plan = None
        if node.type != NodeType.SOURCE:
            build_plan = generate_build_plan(session, node, dialect)
        databases[node] = (node_mat_dbs, build_plan)

    return tree, databases


def _level_database(bp: BuildPlan, levels: List[List[Set[Database]]], level: int = 0):
    """
    takes a build plan and compounds each depth into levels
    """
    if levels is None:
        levels = []
    sub_build_plan = bp[1]
    dbi = reduce(lambda a, b: a & b, (dbs for _, (dbs, _) in sub_build_plan.items()))

    while level >= len(levels):
        levels.append([])
    levels[level].append(dbi)

    for _, (_, sub_sub_build_plan) in sub_build_plan.items():
        if sub_sub_build_plan:
            _level_database(sub_sub_build_plan, levels, level + 1)


async def optimize_level_by_cost(bp: BuildPlan) -> Tuple[int, Database]:
    """
    from a build plan, determine how deep to follow the build plan
    by choosing the lowest cost database
    """
    levels:List[List[Set[Database]]] = []
    _level_database(bp, levels)
    some_db = False
    cheapest_levels = []
    for level in levels:
        try:
            cheapest_levels.append(
                await get_cheapest_online_database(reduce(lambda a, b: a & b, level)),
            )
            some_db = True
        except Exception as exc:
            if "No active database found" in str(exc):
                #maintain levels
                cheapest_levels.append(None)#type: ignore
            else:
                raise exc

    if not some_db:
        raise Exception("No database found that can execute this query.")

    return sorted(
        ((i, cl) for i, cl in enumerate(cheapest_levels)),
        key=lambda icl: icl[1].cost if icl[1] else float("-inf"),
    )[0]


async def optimize_level_by_database_id(
    bp: BuildPlan,
    database_id: int,
) -> Tuple[int, Database]:
    """
    from a build plan, determine how deep to follow the build plan
    by selecting the first level that can run completely in that database
    """

    levels:List[List[Set[Database]]] = []
    _level_database(bp, levels)
    combined_levels = [reduce(lambda a, b: a & b, level) for level in levels]
    for i, level in enumerate(combined_levels):
        for database in level:
            if database.id == database_id and await database.do_ping():
                return i, database
    raise Exception(
        f"The requested database with id {database_id} cannot run this query.",
    )
