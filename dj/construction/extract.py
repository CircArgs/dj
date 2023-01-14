"""
Functions for extracting DJ information from an AST
"""

from typing import Optional, Set, Tuple, Dict, List

from sqlmodel import Session

from dj.construction.compile import CompoundBuildException, compile_query, make_name
from dj.errors import DJError, DJException, ErrorCode
from dj.models.node import Node, NodeType
from dj.sql.parsing import ast
from dj.sql.parsing.backends.sqloxide import parse

def extract_dependencies_from_query(
    session: Session,
    query: ast.Query,
    raise_: bool = True,
) -> Tuple[ast.Query, Set[Node], Set[str]]:
    """Find all dependencies in a compiled query"""
    CompoundBuildException().reset()
    CompoundBuildException().set_raise(False)

    compile_query(session, query)
    deps: Dict[Node, List[ast.Table]] = {}
    danglers: Dict[str, List[ast.Table]] = {}
    for table in query.find_all(ast.Table):
        if node:=table.dj_node:
            deps[node]=deps.get(node) or []
            deps[node].append(table)
        else:
            name = make_name(table.namespace, table.name.name)
            danglers[name]=danglers.get(name) or []
            danglers[name].append(table)

    for col in query.find_all(ast.Column):
        if isinstance(col.table, ast.Table):
            if node := col.table.dj_node:
                if node.type == NodeType.DIMENSION:
                    deps[node]=deps.get(node) or []
                    deps[node].append(col.table)

    if CompoundBuildException().errors and raise_:
        raise DJException(
            message=f"Cannot extract dependencies from query `{query}`",
            errors=CompoundBuildException().errors,
        )
    CompoundBuildException().reset()

    return query, deps, danglers

def extract_dependencies(
    session: Session,
    query: str,
    dialect: Optional[str] = None,
    raise_: bool = True,
) -> Tuple[ast.Query, Set[Node], Set[str]]:
    """Find all dependencies in the a string query"""
    return extract_dependencies_from_query(session, parse(query, dialect), raise_)

def extract_dependencies_from_node(
    session: Session,
    node: Node,
    dialect: Optional[str] = None,
    raise_: bool = True,
) -> Tuple[ast.Query, Set[Node], Set[str]]:
    return extract_dependencies(session, node.query, dialect, raise_)