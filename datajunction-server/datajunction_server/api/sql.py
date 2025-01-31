"""
SQL related APIs.
"""
import logging
from typing import List, Optional

from fastapi import Depends, Query
from sqlmodel import Session

from datajunction_server.api.helpers import (
    build_sql_for_multiple_metrics,
    get_engine,
    get_query,
    validate_orderby,
)
from datajunction_server.internal.authentication.http import SecureAPIRouter
from datajunction_server.models.metric import TranslatedSQL
from datajunction_server.models.query import ColumnMetadata
from datajunction_server.utils import get_session, get_settings

_logger = logging.getLogger(__name__)
settings = get_settings()
router = SecureAPIRouter(tags=["sql"])


@router.get(
    "/sql/{node_name}/",
    response_model=TranslatedSQL,
    name="Get SQL For A Node",
)
def get_sql(
    node_name: str,
    dimensions: List[str] = Query([]),
    filters: List[str] = Query([]),
    orderby: List[str] = Query([]),
    limit: Optional[int] = None,
    *,
    session: Session = Depends(get_session),
    engine_name: Optional[str] = None,
    engine_version: Optional[str] = None,
) -> TranslatedSQL:
    """
    Return SQL for a node.
    """
    engine = (
        get_engine(session, engine_name, engine_version)  # type: ignore
        if engine_name
        else None
    )
    validate_orderby(orderby, [node_name], dimensions)
    query_ast = get_query(
        session=session,
        node_name=node_name,
        dimensions=dimensions,
        filters=filters,
        orderby=orderby,
        limit=limit,
        engine=engine,
    )
    columns = [
        ColumnMetadata(name=col.alias_or_name.name, type=str(col.type))  # type: ignore
        for col in query_ast.select.projection
    ]
    return TranslatedSQL(
        sql=str(query_ast),
        columns=columns,
        dialect=engine.dialect if engine else None,
    )


@router.get("/sql/", response_model=TranslatedSQL, name="Get SQL For Metrics")
def get_sql_for_metrics(
    metrics: List[str] = Query([]),
    dimensions: List[str] = Query([]),
    filters: List[str] = Query([]),
    orderby: List[str] = Query([]),
    limit: Optional[int] = None,
    *,
    session: Session = Depends(get_session),
    engine_name: Optional[str] = None,
    engine_version: Optional[str] = None,
) -> TranslatedSQL:
    """
    Return SQL for a set of metrics with dimensions and filters
    """
    translated_sql, _, _ = build_sql_for_multiple_metrics(
        session,
        metrics,
        dimensions,
        filters,
        orderby,
        limit,
        engine_name,
        engine_version,
    )
    return translated_sql
