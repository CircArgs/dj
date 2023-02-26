# coding: utf-8

"""
    DJ server

    A DataJunction metrics repository  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+gd80c7f5
    Generated by: https://openapi-generator.tech
"""

from djclient.paths.data_availability_node_name_.post import AddAvailabilityDataAvailabilityNodeNamePost
from djclient.paths.catalogs_.post import AddCatalogCatalogsPost
from djclient.paths.nodes_name_columns_column_.post import AddDimensionToNodeNodesNameColumnsColumnPost
from djclient.paths.engines_.post import AddEngineEnginesPost
from djclient.paths.catalogs_name_engines_.post import AddEnginesToCatalogCatalogsNameEnginesPost
from djclient.paths.nodes_name_table_.post import AddTableToNodeNodesNameTablePost
from djclient.paths.nodes_name_tag_.post import AddTagToNodeNodesNameTagPost
from djclient.paths.nodes_.post import CreateNodeNodesPost
from djclient.paths.tags_.post import CreateTagTagsPost
from djclient.paths.nodes_name_downstream_.get import DownstreamNodesNodesNameDownstreamGet
from djclient.paths.tags_name_nodes_.get import FindNodesByTagTagsNameNodesGet
from djclient.paths.graphql.get import HandleHttpGetGraphqlGet
from djclient.paths.graphql.post import HandleHttpPostGraphqlPost
from djclient.paths.health_.get import HealthHealthGet
from djclient.paths.catalogs_.get import ListCatalogsCatalogsGet
from djclient.paths.engines_name_version_.get import ListEngineEnginesNameVersionGet
from djclient.paths.engines_.get import ListEnginesEnginesGet
from djclient.paths.nodes_name_revisions_.get import ListNodeRevisionsNodesNameRevisionsGet
from djclient.paths.tags_.get import ListTagsTagsGet
from djclient.paths.nodes_similarity_node1_name_node2_name.get import NodeSimilarityNodesSimilarityNode1NameNode2NameGet
from djclient.paths.catalogs_name_.get import ReadCatalogCatalogsNameGet
from djclient.paths.cubes_name_.get import ReadCubeCubesNameGet
from djclient.paths.databases_.get import ReadDatabasesDatabasesGet
from djclient.paths.metrics_name_.get import ReadMetricMetricsNameGet
from djclient.paths.metrics_.get import ReadMetricsMetricsGet
from djclient.paths.metrics_name_sql_.get import ReadMetricsSqlMetricsNameSqlGet
from djclient.paths.query_validate.post import ReadMetricsSqlQueryValidatePost
from djclient.paths.nodes_name_.get import ReadNodeNodesNameGet
from djclient.paths.nodes_.get import ReadNodesNodesGet
from djclient.paths.tags_name_.get import ReadTagTagsNameGet
from djclient.paths.nodes_name_.patch import UpdateNodeNodesNamePatch
from djclient.paths.tags_name_.patch import UpdateTagTagsNamePatch
from djclient.paths.nodes_name_materialization_.post import UpsertNodeMaterializationConfigNodesNameMaterializationPost
from djclient.paths.nodes_validate_.post import ValidateNodeNodesValidatePost


class DefaultApi(
    AddAvailabilityDataAvailabilityNodeNamePost,
    AddCatalogCatalogsPost,
    AddDimensionToNodeNodesNameColumnsColumnPost,
    AddEngineEnginesPost,
    AddEnginesToCatalogCatalogsNameEnginesPost,
    AddTableToNodeNodesNameTablePost,
    AddTagToNodeNodesNameTagPost,
    CreateNodeNodesPost,
    CreateTagTagsPost,
    DownstreamNodesNodesNameDownstreamGet,
    FindNodesByTagTagsNameNodesGet,
    HandleHttpGetGraphqlGet,
    HandleHttpPostGraphqlPost,
    HealthHealthGet,
    ListCatalogsCatalogsGet,
    ListEngineEnginesNameVersionGet,
    ListEnginesEnginesGet,
    ListNodeRevisionsNodesNameRevisionsGet,
    ListTagsTagsGet,
    NodeSimilarityNodesSimilarityNode1NameNode2NameGet,
    ReadCatalogCatalogsNameGet,
    ReadCubeCubesNameGet,
    ReadDatabasesDatabasesGet,
    ReadMetricMetricsNameGet,
    ReadMetricsMetricsGet,
    ReadMetricsSqlMetricsNameSqlGet,
    ReadMetricsSqlQueryValidatePost,
    ReadNodeNodesNameGet,
    ReadNodesNodesGet,
    ReadTagTagsNameGet,
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
