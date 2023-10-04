"""
Dimensions related APIs.
"""
import logging
from typing import List, Optional, Union, Set

from fastapi import Depends, Query
from sqlmodel import Session
from typing_extensions import Annotated

from datajunction_server.api.helpers import get_node_by_name
from datajunction_server.api.nodes import list_nodes
from datajunction_server.internal.authentication.http import SecureAPIRouter
from datajunction_server.models.node import NodeRevisionOutput, NodeType
from datajunction_server.sql.dag import (
    get_nodes_with_common_dimensions,
    get_nodes_with_dimension,
)
from datajunction_server.utils import get_session, get_settings
from datajunction_server.utils import (
    get_current_user,
    get_query_service_client,
    get_session,
    get_settings,
)
from datajunction_server.models import History, User
from datajunction_server.models import access
from datajunction_server.models.access import validate_access

settings = get_settings()
_logger = logging.getLogger(__name__)
router = SecureAPIRouter(tags=["dimensions"])


@router.get("/dimensions/", response_model=List[str])
def list_dimensions(
    prefix: Optional[str] = None, *, session: Session = Depends(get_session)
) -> List[str]:
    """
    List all available dimensions.
    """
    return list_nodes(node_type=NodeType.DIMENSION, prefix=prefix, session=session)


@router.get("/dimensions/{name}/nodes/", response_model=List[NodeRevisionOutput])
def find_nodes_with_dimension(
    name: str,
    *,
    node_type: Annotated[Union[List[NodeType], None], Query()] = Query(None),
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user),
    validate_access: access.ValidateAccessFn = Depends(validate_access)
) -> List[NodeRevisionOutput]:
    """
    List all nodes that have the specified dimension
    """
    dimension_node = get_node_by_name(session, name)
    nodes = get_nodes_with_dimension(session, dimension_node, node_type)

    access_control = access.AccessControl(
        validate_access = validate_access,
        user = current_user,
    )
    for node in nodes:
        access_control.add_request_by_node(node)

    validation_results = access_control.validate()

    return [request.resource_object for request in validation_results if request.approved]


@router.get("/dimensions/common/", response_model=List[NodeRevisionOutput])
def find_nodes_with_common_dimensions(
    dimension: Annotated[Union[List[str], None], Query()] = Query(None),
    node_type: Annotated[Union[List[NodeType], None], Query()] = Query(None),
    *,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user),
    validate_access: access.ValidateAccessFn = Depends(validate_access)
) -> List[NodeRevisionOutput]:
    """
    Find all nodes that have the list of common dimensions
    """
    nodes = get_nodes_with_common_dimensions(
        session,
        [get_node_by_name(session, dim) for dim in dimension],  # type: ignore
        node_type,
    )
    access_control = access.AccessControl(
        validate_access = validate_access,
        user = current_user,
    )
    for node in nodes:
        access_control.add_request_by_node(node)

    validation_results = access_control.validate()

    return [request.resource_object for request in validation_results if request.approved]

