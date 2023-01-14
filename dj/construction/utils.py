"""
Utilities used around construction
"""

from typing import Iterable, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from dj.errors import DJError, DJException, ErrorCode
from dj.models.node import Node, NodeType
from dj.sql.parsing.ast import Namespace
from dj.construction.exceptions import CompoundBuildException


def make_name(namespace: Optional[Namespace], name="") -> str:
    """utility taking a namespace and name to make a possible name of a DJ Node"""
    ret = ""
    if namespace:
        ret += ".".join(name.name for name in namespace.names)
    if name:
        ret += ("." if ret else "") + name
    return ret

def get_dj_node(
    session: Session,
    node_name: str,
    kinds: Optional[Iterable[NodeType]] = None,
) -> Optional[Node]:
    """Return the DJ Node with a given name from a set of node types"""
    query = select(Node).filter(Node.name == node_name)
    match = None
    try:
        match = session.exec(query).one()
    except NoResultFound:
        kind_msg = " or ".join(str(k) for k in kinds) if kinds else ""
        CompoundBuildException().append(
            error=DJError(
                code=ErrorCode.UNKNOWN_NODE,
                message=f"No node `{node_name}` exists of kind {kind_msg}.",
            ),
            message=f"Cannot get DJ node {node_name}",
        )

    if match and kinds and (match.type not in kinds):
        CompoundBuildException().append(
            error=DJError(
                code=ErrorCode.NODE_TYPE_ERROR,
                message=(
                    f"Node `{match.name}` is of type `{str(match.type).upper()}`. "
                    "Expected kind to be of {' or '.join(str(k) for k in kinds)}."
                ),
            ),
            message=f"Cannot get DJ node {node_name}",
        )

    return match


