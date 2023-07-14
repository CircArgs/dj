"""
Model for history.
"""
from datetime import datetime, timezone
from enum import Enum
from functools import partial
from typing import Any, Dict, Optional

from sqlalchemy import DateTime
from sqlalchemy.sql.schema import Column as SqlaColumn
from sqlmodel import JSON, Field, SQLModel

from datajunction_server.typing import UTCDatetime


class ActivityType(str, Enum):
    """
    An activity type
    """

    CREATE = "create"
    DELETE = "delete"
    RESTORE = "restore"
    UPDATE = "update"
    TAG = "tag"
    SET_ATTRIBUTE = "set_attribute"


class EntityType(str, Enum):
    """
    An entity type for which activity can occur
    """

    ATTRIBUTE = "attribute"
    AVAILABILITY = "availability"
    CATALOG = "catalog"
    COLUMN_ATTRIBUTE = "column_attribute"
    ENGINE = "engine"
    LINK = "link"
    MATERIALIZATION = "materialization"
    NAMESPACE = "namespace"
    NODE = "node"
    QUERY = "query"
    TAG = "tag"


class History(SQLModel, table=True):  # type: ignore
    """
    An event to store as part of the server's activity history
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    entity_type: Optional[EntityType] = Field(default=None)
    entity_name: Optional[str] = Field(default=None)
    context_node: Optional[str] = Field(default=None)
    activity_type: Optional[ActivityType] = Field(default=None)
    user: Optional[str] = Field(default=None)
    pre: Dict[str, Any] = Field(default_factory=dict, sa_column=SqlaColumn(JSON))
    post: Dict[str, Any] = Field(default_factory=dict, sa_column=SqlaColumn(JSON))
    details: Dict[str, Any] = Field(default_factory=dict, sa_column=SqlaColumn(JSON))
    created_at: UTCDatetime = Field(
        sa_column=SqlaColumn(DateTime(timezone=True)),
        default_factory=partial(datetime.now, timezone.utc),
    )

    def __hash__(self) -> int:
        return hash(self.id)
