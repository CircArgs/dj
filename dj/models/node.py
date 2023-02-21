"""
Model for nodes.
"""

import enum
from collections import defaultdict
from datetime import datetime, timezone
from functools import partial
from typing import Dict, List, Optional, cast

from pydantic import BaseModel, Extra
from pydantic import Field as PydanticField
from sqlalchemy import JSON, DateTime, String
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy.sql.schema import Column as SqlaColumn
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.types import Enum
from sqlmodel import Field, Relationship, SQLModel
from typing_extensions import TypedDict

from dj.models.base import BaseSQLModel
from dj.models.catalog import Catalog
from dj.models.column import Column, ColumnYAML
from dj.models.database import Database
from dj.models.engine import Engine, EngineInfo
from dj.models.table import Table, TableNodeRevision, TableYAML
from dj.sql.parse import is_metric
from dj.typing import ColumnType
from dj.utils import UTCDatetime, Version

DEFAULT_DRAFT_VERSION = Version(major=0, minor=1)
DEFAULT_PUBLISHED_VERSION = Version(major=1, minor=0)


class NodeRelationship(BaseSQLModel, table=True):  # type: ignore
    """
    Join table for self-referential many-to-many relationships between nodes.
    """

    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="node.id",
        primary_key=True,
    )

    # This will default to `latest`, which points to the current version of the node,
    # or it can be a specific version.
    parent_version: Optional[str] = Field(
        default="latest",
    )

    child_id: Optional[int] = Field(
        default=None,
        foreign_key="noderevision.id",
        primary_key=True,
    )


class CubeRelationship(BaseSQLModel, table=True):  # type: ignore
    """
    Join table for many-to-many relationships between cube nodes and metric/dimension nodes.
    """

    cube_id: Optional[int] = Field(
        default=None,
        foreign_key="noderevision.id",
        primary_key=True,
    )

    cube_element_id: Optional[int] = Field(
        default=None,
        foreign_key="node.id",
        primary_key=True,
    )


class NodeColumns(BaseSQLModel, table=True):  # type: ignore
    """
    Join table for node columns.
    """

    node_id: Optional[int] = Field(
        default=None,
        foreign_key="noderevision.id",
        primary_key=True,
    )
    column_id: Optional[int] = Field(
        default=None,
        foreign_key="column.id",
        primary_key=True,
    )


class NodeType(str, enum.Enum):
    """
    Node type.

    A node can have 4 types, currently:

    1. SOURCE nodes are root nodes in the DAG, and point to tables or views in a DB.
    2. TRANSFORM nodes are SQL transformations, reading from SOURCE/TRANSFORM nodes.
    3. METRIC nodes are leaves in the DAG, and have a single aggregation query.
    4. DIMENSION nodes are special SOURCE nodes that can be auto-joined with METRICS.
    5. CUBE nodes contain a reference to a set of METRICS and a set of DIMENSIONS.
    """

    SOURCE = "source"
    TRANSFORM = "transform"
    METRIC = "metric"
    DIMENSION = "dimension"
    CUBE = "cube"


class NodeMode(str, enum.Enum):
    """
    Node mode.

    A node can be in one of the following modes:

    1. PUBLISHED - Must be valid and not cause any child nodes to be invalid
    2. DRAFT - Can be invalid, have invalid parents, and include dangling references
    """

    PUBLISHED = "published"
    DRAFT = "draft"


class NodeStatus(str, enum.Enum):
    """
    Node status.

    A node can have one of the following statuses:

    1. VALID - All references to other nodes and node columns are valid
    2. INVALID - One or more parent nodes are incompatible or do not exist
    """

    VALID = "valid"
    INVALID = "invalid"


class NodeYAML(TypedDict, total=False):
    """
    Schema of a node in the YAML file.
    """

    description: str
    display_name: str
    type: NodeType
    query: str
    columns: Dict[str, ColumnYAML]
    tables: Dict[str, List[TableYAML]]


def labelize(value: str) -> str:
    """
    Turn a system name into a human-readable name.
    """

    return value.replace(".", ": ").replace("_", " ").title()


def generate_display_name(column_name: str):
    """
    SQLAlchemy helper to generate a human-readable version of the given system name.
    """

    def default_function(context: DefaultExecutionContext) -> str:
        column_value = context.current_parameters.get(column_name)
        return labelize(column_value)

    return default_function


class NodeBase(BaseSQLModel):
    """
    A base node.
    """

    name: str = Field(sa_column=SqlaColumn("name", String, unique=True))
    type: NodeType = Field(sa_column=SqlaColumn(Enum(NodeType)))
    display_name: Optional[str] = Field(
        sa_column=SqlaColumn(
            "display_name",
            String,
            default=generate_display_name("name"),
        ),
        max_length=100,
    )


class NodeRevisionBase(BaseSQLModel):
    """
    A base node revision.
    """

    name: str = Field(
        sa_column=SqlaColumn("name", String, unique=False),
        foreign_key="node.name",
    )
    display_name: Optional[str] = Field(
        sa_column=SqlaColumn(
            "display_name",
            String,
            default=generate_display_name("name"),
        ),
    )
    type: NodeType = Field(sa_column=SqlaColumn(Enum(NodeType)))
    description: str = ""
    query: Optional[str] = None
    mode: NodeMode = NodeMode.PUBLISHED


class MissingParent(BaseSQLModel, table=True):  # type: ignore
    """
    A missing parent node
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=SqlaColumn("name", String))
    created_at: UTCDatetime = Field(
        sa_column=SqlaColumn(DateTime(timezone=True)),
        default_factory=partial(datetime.now, timezone.utc),
    )


class NodeMissingParents(BaseSQLModel, table=True):  # type: ignore
    """
    Join table for missing parents
    """

    missing_parent_id: Optional[int] = Field(
        default=None,
        foreign_key="missingparent.id",
        primary_key=True,
    )
    referencing_node_id: Optional[int] = Field(
        default=None,
        foreign_key="noderevision.id",
        primary_key=True,
    )


class AvailabilityStateBase(BaseSQLModel):
    """
    An availability state base
    """

    catalog: str
    schema_: Optional[str] = Field(default=None)
    table: str
    valid_through_ts: int
    max_partition: List[str] = Field(sa_column=SqlaColumn(JSON))
    min_partition: List[str] = Field(sa_column=SqlaColumn(JSON))


class AvailabilityState(AvailabilityStateBase, table=True):  # type: ignore
    """
    The availability of materialized data for a node
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    updated_at: UTCDatetime = Field(
        sa_column=SqlaColumn(DateTime(timezone=True)),
        default_factory=partial(datetime.now, timezone.utc),
    )


class NodeAvailabilityState(BaseSQLModel, table=True):  # type: ignore
    """
    Join table for availability state
    """

    availability_id: Optional[int] = Field(
        default=None,
        foreign_key="availabilitystate.id",
        primary_key=True,
    )
    node_id: Optional[int] = Field(
        default=None,
        foreign_key="noderevision.id",
        primary_key=True,
    )


class Node(NodeBase, table=True):  # type: ignore
    """
    Node that acts as an umbrella for all node revisions
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    current_version: str = Field(default=str(DEFAULT_DRAFT_VERSION))
    created_at: UTCDatetime = Field(
        sa_column=SqlaColumn(DateTime(timezone=True)),
        default_factory=partial(datetime.now, timezone.utc),
    )

    revisions: List["NodeRevision"] = Relationship(back_populates="node")
    cubes: List["NodeRevision"] = Relationship(back_populates="cube_elements")
    current: "NodeRevision" = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "and_(Node.id==NodeRevision.node_id, "
            "Node.current_version == NodeRevision.version)",
            "viewonly": True,
            "uselist": False,
        },
    )

    children: List["NodeRevision"] = Relationship(
        back_populates="parents",
        link_model=NodeRelationship,
        sa_relationship_kwargs={
            "primaryjoin": "Node.id==NodeRelationship.parent_id",
            "secondaryjoin": "NodeRevision.id==NodeRelationship.child_id",
        },
    )

    def __hash__(self) -> int:
        return hash(self.id)


class MaterializationConfig(BaseSQLModel, table=True):  # type: ignore
    """
    Materialization configuration for a node and specific engines.
    """

    node_revision_id: int = Field(foreign_key="noderevision.id", primary_key=True)
    node_revision: "NodeRevision" = Relationship(
        back_populates="materialization_configs",
    )

    engine_id: int = Field(foreign_key="engine.id", primary_key=True)
    engine: Engine = Relationship()

    config: str = Field(nullable=False)


class NodeRevision(NodeRevisionBase, table=True):  # type: ignore
    """
    A node revision.
    """

    __table_args__ = (UniqueConstraint("version", "node_id"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    version: Optional[str] = Field(default=str(DEFAULT_DRAFT_VERSION))
    node_id: Optional[int] = Field(foreign_key="node.id")
    node: Node = Relationship(back_populates="revisions")
    cube_elements: List["Node"] = Relationship(  # Only used by cube nodes
        back_populates="cubes",
        link_model=CubeRelationship,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==CubeRelationship.cube_id",
            "secondaryjoin": "Node.id==CubeRelationship.cube_element_id",
            "lazy": "joined",
        },
    )
    status: NodeStatus = NodeStatus.INVALID
    updated_at: UTCDatetime = Field(
        sa_column=SqlaColumn(DateTime(timezone=True)),
        default_factory=partial(datetime.now, timezone.utc),
    )

    tables: List[Table] = Relationship(
        back_populates="node",
        link_model=TableNodeRevision,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==TableNodeRevision.node_revision_id",
            "secondaryjoin": "Table.id==TableNodeRevision.table_id",
            "cascade": "all, delete",
        },
    )

    parents: List["Node"] = Relationship(
        back_populates="children",
        link_model=NodeRelationship,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==NodeRelationship.child_id",
            "secondaryjoin": "Node.id==NodeRelationship.parent_id",
        },
    )

    parent_links: List[NodeRelationship] = Relationship()

    missing_parents: List[MissingParent] = Relationship(
        link_model=NodeMissingParents,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==NodeMissingParents.referencing_node_id",
            "secondaryjoin": "MissingParent.id==NodeMissingParents.missing_parent_id",
            "cascade": "all, delete",
        },
    )

    columns: List[Column] = Relationship(
        link_model=NodeColumns,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==NodeColumns.node_id",
            "secondaryjoin": "Column.id==NodeColumns.column_id",
            "cascade": "all, delete",
        },
    )

    # The availability of materialized data needs to be stored on the NodeRevision
    # level in order to support pinned versions, where a node owner wants to pin
    # to a particular upstream node version.
    availability: Optional[AvailabilityState] = Relationship(
        link_model=NodeAvailabilityState,
        sa_relationship_kwargs={
            "primaryjoin": "NodeRevision.id==NodeAvailabilityState.node_id",
            "secondaryjoin": "AvailabilityState.id==NodeAvailabilityState.availability_id",
            "cascade": "all, delete",
            "uselist": False,
        },
    )

    # Nodes of type SOURCE will not have this property as their materialization
    # is not managed as a part of this service
    materialization_configs: List[MaterializationConfig] = Relationship(
        back_populates="node_revision",
    )

    def to_yaml(self) -> NodeYAML:
        """
        Serialize the node for YAML.

        This is used to update the original configuration with information about columns.
        """
        tables = defaultdict(list)
        for table in self.tables:  # pylint: disable=not-an-iterable
            tables[table.database.name].append(table.to_yaml())

        data = {
            "description": self.description,
            "display_name": self.display_name,
            "type": self.type.value,  # pylint: disable=no-member
            "query": self.query,
            "columns": {
                column.name: column.to_yaml()
                for column in self.columns  # pylint: disable=not-an-iterable
            },
            "tables": dict(tables),
        }
        filtered = {key: value for key, value in data.items() if value}

        return cast(NodeYAML, filtered)

    def __hash__(self) -> int:
        return hash(self.id)

    def extra_validation(self) -> None:
        """
        Extra validation for node data.
        """
        if self.type in (NodeType.SOURCE, NodeType.CUBE):
            if self.query:
                raise Exception(
                    f"Node {self.name} of type {self.type} should not have a query",
                )

        if self.type in {NodeType.TRANSFORM, NodeType.METRIC, NodeType.DIMENSION}:
            if not self.query:
                raise Exception(
                    f"Node {self.name} of type {self.type} needs a query",
                )

        if self.type == NodeType.METRIC:
            if not is_metric(self.query):
                raise Exception(
                    f"Node {self.name} of type metric has an invalid query, "
                    "should have a single aggregation",
                )

        if self.type == NodeType.CUBE:
            if not self.cube_elements:
                raise Exception(
                    f"Node {self.name} of type cube node needs cube elements",
                )


class ImmutableNodeFields(BaseSQLModel):
    """
    Node fields that cannot be changed
    """

    name: str
    type: NodeType


class MutableNodeFields(BaseSQLModel):
    """
    Node fields that can be changed.
    """

    display_name: Optional[str]
    description: str
    query: Optional[str]
    mode: NodeMode


class SourceNodeColumnType(TypedDict, total=False):
    """
    Schema of a column for a table defined in a source node
    """

    type: ColumnType
    dimension: Optional[str]


class SourceNodeFields(BaseSQLModel):
    """
    Source node fields that can be changed.
    """

    columns: Dict[str, SourceNodeColumnType]


class CubeNodeFields(BaseSQLModel):
    """
    Cube node fields that can be changed
    """

    display_name: Optional[str]
    cube_elements: List[str]
    description: str
    mode: NodeMode


#
# Create and Update objects
#


class CreateNode(ImmutableNodeFields, MutableNodeFields):
    """
    Create non-source node object.
    """


class CreateSourceNode(ImmutableNodeFields, MutableNodeFields, SourceNodeFields):
    """
    A create object for source nodes
    """


class CreateCubeNode(ImmutableNodeFields, CubeNodeFields):
    """
    A create object for cube nodes
    """


class UpdateNode(MutableNodeFields, SourceNodeFields):
    """
    Update node object where all fields are optional
    """

    __annotations__ = {
        k: Optional[v]
        for k, v in {
            **SourceNodeFields.__annotations__,  # pylint: disable=E1101
            **MutableNodeFields.__annotations__,  # pylint: disable=E1101
        }.items()
    }

    class Config:  # pylint: disable=too-few-public-methods
        """
        Do not allow fields other than the ones defined here.
        """

        extra = Extra.forbid


class UpsertMaterializationConfig(BaseSQLModel):
    """
    An upsert object for materialization configs
    """

    engine_name: str
    engine_version: str
    config: str


#
# Response output objects
#


class OutputModel(BaseModel):
    """
    An output model with the ability to flatten fields. When fields are created with
    `Field(flatten=True)`, the field's values will be automatically flattened into the
    parent output model.
    """

    def _iter(self, *args, to_dict: bool = False, **kwargs):
        for dict_key, value in super()._iter(to_dict, *args, **kwargs):
            if to_dict and self.__fields__[dict_key].field_info.extra.get(
                "flatten",
                False,
            ):
                assert isinstance(value, dict)
                for key, val in value.items():
                    yield key, val
            else:
                yield dict_key, value


class SimpleColumn(SQLModel):
    """
    A simplified column schema, without ID or dimensions.
    """

    name: str
    type: ColumnType


class TableOutput(SQLModel):
    """
    Output for table information.
    """

    id: Optional[int]
    catalog: Optional[Catalog]
    schema_: Optional[str]
    table: Optional[str]
    database: Optional[Database]


class MaterializationConfigOutput(SQLModel):
    """
    Output for materialization config.
    """

    engine: EngineInfo
    config: str


class NodeRevisionOutput(SQLModel):
    """
    Output for a node revision with information about columns and if it is a metric.
    """

    id: int = Field(alias="node_revision_id")
    node_id: int
    type: NodeType
    name: str
    display_name: str
    version: str
    description: str = ""
    query: Optional[str] = None
    availability: Optional[AvailabilityState] = None
    columns: List[SimpleColumn]
    tables: List[TableOutput]
    updated_at: UTCDatetime
    materialization_configs: List[MaterializationConfigOutput]

    class Config:  # pylint: disable=missing-class-docstring,too-few-public-methods
        allow_population_by_field_name = True


class NodeOutput(OutputModel):
    """
    Output for a node that shows the current revision.
    """

    current: NodeRevisionOutput = PydanticField(flatten=True)
    created_at: UTCDatetime


class NodeValidation(SQLModel):
    """
    A validation of a provided node definition
    """

    message: str
    status: NodeStatus
    node: Node
    node_revision: NodeRevision
    dependencies: List[NodeRevisionOutput]
    columns: List[Column]
