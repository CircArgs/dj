# coding: utf-8

"""
    DJ server

    A DataJunction metrics layer  # noqa: E501

    The version of the OpenAPI document: 0.0.post1.dev1+g7c4b316
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


class UpsertMaterializationConfig(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    An upsert object for materialization configs
    """


    class MetaOapg:
        required = {
            "engine_name",
            "engine_version",
            "config",
        }
        
        class properties:
            engine_name = schemas.StrSchema
            engine_version = schemas.StrSchema
            config = schemas.StrSchema
            __annotations__ = {
                "engine_name": engine_name,
                "engine_version": engine_version,
                "config": config,
            }
    
    engine_name: MetaOapg.properties.engine_name
    engine_version: MetaOapg.properties.engine_version
    config: MetaOapg.properties.config
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["engine_name"]) -> MetaOapg.properties.engine_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["engine_version"]) -> MetaOapg.properties.engine_version: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["config"]) -> MetaOapg.properties.config: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["engine_name", "engine_version", "config", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["engine_name"]) -> MetaOapg.properties.engine_name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["engine_version"]) -> MetaOapg.properties.engine_version: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["config"]) -> MetaOapg.properties.config: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["engine_name", "engine_version", "config", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        engine_name: typing.Union[MetaOapg.properties.engine_name, str, ],
        engine_version: typing.Union[MetaOapg.properties.engine_version, str, ],
        config: typing.Union[MetaOapg.properties.config, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UpsertMaterializationConfig':
        return super().__new__(
            cls,
            *_args,
            engine_name=engine_name,
            engine_version=engine_version,
            config=config,
            _configuration=_configuration,
            **kwargs,
        )
