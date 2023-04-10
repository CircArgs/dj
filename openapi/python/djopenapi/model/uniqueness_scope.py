# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+g6ea8804
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

from djopenapi import schemas  # noqa: F401


class UniquenessScope(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The scope at which this attribute needs to be unique.
    """


    class MetaOapg:
        enum_value_to_name = {
            "node": "NODE",
            "column_type": "COLUMN_TYPE",
        }
    
    @schemas.classproperty
    def NODE(cls):
        return cls("node")
    
    @schemas.classproperty
    def COLUMN_TYPE(cls):
        return cls("column_type")
