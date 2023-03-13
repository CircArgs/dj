# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+g7c4b316
    Generated by: https://openapi-generator.tech
"""

from djclient.paths.attributes_.post import AddAttributeTypeAttributesPost
from djclient.paths.data_availability_node_name_.post import AddAvailabilityDataAvailabilityNodeNamePost
from djclient.paths.catalogs_.post import AddCatalogCatalogsPost
from djclient.paths.nodes_name_columns_column_.post import AddDimensionToNodeNodesNameColumnsColumnPost
from djclient.paths.engines_.post import AddEngineEnginesPost
from djclient.paths.catalogs_name_engines_.post import AddEnginesToCatalogCatalogsNameEnginesPost
from djclient.paths.nodes_name_tag_.post import AddTagToNodeNodesNameTagPost
from djclient.paths.metrics_common_dimensions_.get import CommonDimensionsMetricsCommonDimensionsGet
from djclient.paths.nodes_cube_.post import CreateCubeNodeNodesCubePost
from djclient.paths.nodes_dimension_.post import CreateNodeNodesDimensionPost
from djclient.paths.nodes_metric_.post import CreateNodeNodesMetricPost
from djclient.paths.nodes_transform_.post import CreateNodeNodesTransformPost
from djclient.paths.nodes_source_.post import CreateSourceNodeNodesSourcePost
from djclient.paths.tags_.post import CreateTagTagsPost
from djclient.paths.nodes_name_downstream_.get import DownstreamNodesNodesNameDownstreamGet
from djclient.paths.tags_name_nodes_.get import FindNodesByTagTagsNameNodesGet
from djclient.paths.health_.get import HealthHealthGet
from djclient.paths.attributes_.get import ListAttributesAttributesGet
from djclient.paths.catalogs_.get import ListCatalogsCatalogsGet
from djclient.paths.engines_name_version_.get import ListEngineEnginesNameVersionGet
from djclient.paths.engines_.get import ListEnginesEnginesGet
from djclient.paths.nodes_name_revisions_.get import ListNodeRevisionsNodesNameRevisionsGet
from djclient.paths.tags_.get import ListTagsTagsGet
from djclient.paths.nodes_similarity_node1_name_node2_name.get import NodeSimilarityNodesSimilarityNode1NameNode2NameGet
from djclient.paths.catalogs_name_.get import ReadCatalogCatalogsNameGet
from djclient.paths.cubes_name_.get import ReadCubeCubesNameGet
from djclient.paths.metrics_name_.get import ReadMetricMetricsNameGet
from djclient.paths.metrics_.get import ReadMetricsMetricsGet
from djclient.paths.metrics_name_sql_.get import ReadMetricsSqlMetricsNameSqlGet
from djclient.paths.query_sql.get import ReadMetricsSqlQuerySqlGet
from djclient.paths.nodes_name_.get import ReadNodeNodesNameGet
from djclient.paths.nodes_.get import ReadNodesNodesGet
from djclient.paths.tags_name_.get import ReadTagTagsNameGet
from djclient.paths.nodes_node_name_attributes_.post import SetColumnAttributesNodesNodeNameAttributesPost
from djclient.paths.nodes_name_.patch import UpdateNodeNodesNamePatch
from djclient.paths.tags_name_.patch import UpdateTagTagsNamePatch
from djclient.paths.nodes_name_materialization_.post import UpsertNodeMaterializationConfigNodesNameMaterializationPost
from djclient.paths.nodes_validate_.post import ValidateNodeNodesValidatePost


class DefaultApi(
    AddAttributeTypeAttributesPost,
    AddAvailabilityDataAvailabilityNodeNamePost,
    AddCatalogCatalogsPost,
    AddDimensionToNodeNodesNameColumnsColumnPost,
    AddEngineEnginesPost,
    AddEnginesToCatalogCatalogsNameEnginesPost,
    AddTagToNodeNodesNameTagPost,
    CommonDimensionsMetricsCommonDimensionsGet,
    CreateCubeNodeNodesCubePost,
    CreateNodeNodesDimensionPost,
    CreateNodeNodesMetricPost,
    CreateNodeNodesTransformPost,
    CreateSourceNodeNodesSourcePost,
    CreateTagTagsPost,
    DownstreamNodesNodesNameDownstreamGet,
    FindNodesByTagTagsNameNodesGet,
    HealthHealthGet,
    ListAttributesAttributesGet,
    ListCatalogsCatalogsGet,
    ListEngineEnginesNameVersionGet,
    ListEnginesEnginesGet,
    ListNodeRevisionsNodesNameRevisionsGet,
    ListTagsTagsGet,
    NodeSimilarityNodesSimilarityNode1NameNode2NameGet,
    ReadCatalogCatalogsNameGet,
    ReadCubeCubesNameGet,
    ReadMetricMetricsNameGet,
    ReadMetricsMetricsGet,
    ReadMetricsSqlMetricsNameSqlGet,
    ReadMetricsSqlQuerySqlGet,
    ReadNodeNodesNameGet,
    ReadNodesNodesGet,
    ReadTagTagsNameGet,
    SetColumnAttributesNodesNodeNameAttributesPost,
    UpdateNodeNodesNamePatch,
    UpdateTagTagsNamePatch,
    UpsertNodeMaterializationConfigNodesNameMaterializationPost,
    ValidateNodeNodesValidatePost,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
