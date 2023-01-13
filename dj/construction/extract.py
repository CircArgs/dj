"""
Functions for extracting DJ information from an AST
"""

from typing import Optional, Set, Tuple

from sqlmodel import Session

from dj.construction.compile import CompoundBuildException, compile_query, make_name
from dj.errors import DJError, DJException, ErrorCode
from dj.models import Node
from dj.sql.parsing import ast
from dj.sql.parsing.backends.sqloxide import parse


def extract_dependencies(
    session: Session,
    query: str,
    dialect: Optional[str] = None,
    raise_: bool = True,
) -> Tuple[ast.Query, Set[Node], Set[str]]:
    """Find all dependencies in the dj dag of a node"""
    CompoundBuildException().reset()
    CompoundBuildException().set_raise(False)

    tree = parse(query, dialect)
    compile_query(session, tree)
    deps, danglers = set(), set()
    for table in tree.find_all(ast.Table):
        if table.dj_node:
            deps.add(table.dj_node)
        else:
            danglers.add(make_name(table.namespace, table.name.name))

    if CompoundBuildException().errors and raise_:
        raise DJException(
            message=f"Cannot extract dependencies from query `{query}`",
            errors=CompoundBuildException().errors,
        )
    CompoundBuildException().reset()

    return tree, deps, danglers
