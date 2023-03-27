from typing import List, Optional

from sqlmodel import Session

from dj.models.node import BuildCriteria
from dj.sql.parsing import ast2, parse

def build_node(  # pylint: disable=too-many-arguments
    session: Session,
    metrics: List[str],
    dimensions: Optional[List[str]] = None,
    filters: Optional[List[str]] = None,
    dialect: Optional[str] = None,
    build_criteria: Optional[BuildCriteria] = None,
) -> ast2.Query:
    """
    Builds a Query AST
    """
