"""
tools for planning the steps a node will need to take to be built to run
"""
from dj.construction.extract import extract_dependencies
from dj.sql.parsing import ast
from dj.models.node import Node, NodeType
from dj.models.database import Database
from dj.sql.dag import get_cheapest_online_database
from typing import Set, List, Dict, Optional, Tuple
from functools import reduce

from sqlmodel import Session
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

BuildPlan = Tuple[ast.Query, Dict[Node, Tuple[Set[Database], "BuildPlan"]]]

def generate_build_plan(session: Session, node: Node, dialect: Optional[str] = None) -> BuildPlan:
    """
    Returns the list of optimal databases in order of decreasing goodness

    gooder firster
    """

    tree, deps, _ = extract_dependencies(session, node.query, dialect)
    databases = {}
    for node, tables in deps.items():
        columns = {col.name.name for table in tables for col in table.columns}

        node_mat_dbs = get_node_materialized_databases(node, columns)
        build_plan = None
        if node.type != NodeType.SOURCE:
            build_plan = generate_build_plan(node, dialect)
        databases[node] = (node_mat_dbs, build_plan)

    return tree, databases

def _level_database(bp: BuildPlan, levels: List[List[Set[Database]]], level: int = 0):
    """
    takes a build plan and compounds each depth into a levels
    """
    if levels is None:
        levels = []
    tree, sbp = bp
    nodes = set((node for node, _ in sbp.items()))
    dbi = reduce(lambda a, b: a & b, (dbs for _, (dbs, _) in sbp.items()))

    while level >= len(levels):
        levels.append([])
    levels[level].append(dbi)

    for _, (_, ssbp) in sbp.items():
        if ssbp:
            level_database(ssbp, levels, level + 1)

async def optimize_level_by_cost(bp: BuildPlan) -> Tuple[int, Database]:
    """
    from a build plan, determine how deep to follow the build plan by choosing the lowest cost database
    """
    levels = []
    _level_database(bp, levels)
    some_db = False
    cheapest_levels = []
    for level in levels:
        try:
            cheapest_levels.append(
                await get_cheapest_online_database(reduce(lambda a, b: a & b, level))
            )
            some_db = True
        except Exception as exc:
            if "No active database found" in str(exc):
                cheapest_levels.append(None)
            else:
                raise exc

    if not some_db:
        raise Exception("No database found that can execute this query.")

    return sorted(
        ((i, cl) for i, cl in enumerate(cheapest_levels)),
        key=lambda icl: icl[1].cost if icl[1] else float("-inf"),
    )[0]

async def optimize_level_by_database_id(bp: BuildPlan, database_id: int) -> Tuple[int, Database]:
    """
    from a build plan, determine how deep to follow the build plan 
    by selecting the first level that can run completely in that database
    """
    levels = []
    _level_database(bp, levels)
    some_db = False
    combined_levels = [reduce(lambda a, b: a & b, level) for level in levels]
    for i, level in enumerate(combined_levels):
        for database in level:
            if database.id == database_id and await database.do_ping():
                return i, database
    raise Exception(f"The requested database with id {database_id} cannot run this query.")
