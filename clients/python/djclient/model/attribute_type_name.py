# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+gfdbe207
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


class AttributeTypeName(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attribute type name.
    """


    class MetaOapg:
        required = {
            "name",
            "namespace",
        }
        
        class properties:
            namespace = schemas.StrSchema
            name = schemas.StrSchema
            __annotations__ = {
                "namespace": namespace,
                "name": name,
            }
    
    name: MetaOapg.properties.name
    namespace: MetaOapg.properties.namespace
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["namespace"]) -> MetaOapg.properties.namespace: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["namespace", "name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["namespace"]) -> MetaOapg.properties.namespace: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["namespace", "name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        namespace: typing.Union[MetaOapg.properties.namespace, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AttributeTypeName':
        return super().__new__(
            cls,
            *_args,
            name=name,
            namespace=namespace,
            _configuration=_configuration,
            **kwargs,
        )
