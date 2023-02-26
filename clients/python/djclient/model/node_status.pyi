# coding: utf-8

"""
    DJ server

    A DataJunction metrics repository  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+gd80c7f5
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from djclient import schemas  # noqa: F401


class NodeStatus(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Node status.

A node can have one of the following statuses:

1. VALID - All references to other nodes and node columns are valid
2. INVALID - One or more parent nodes are incompatible or do not exist
    """
    
    @schemas.classproperty
    def VALID(cls):
        return cls("valid")
    
    @schemas.classproperty
    def INVALID(cls):
        return cls("invalid")
