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


class UpdateTag(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Update tag model. Only works on mutable fields.
    """


    class MetaOapg:
        
        class properties:
            description = schemas.StrSchema
            tag_metadata = schemas.DictSchema
            __annotations__ = {
                "description": description,
                "tag_metadata": tag_metadata,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tag_metadata"]) -> MetaOapg.properties.tag_metadata: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["description"], typing_extensions.Literal["tag_metadata"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tag_metadata"]) -> typing.Union[MetaOapg.properties.tag_metadata, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["description"], typing_extensions.Literal["tag_metadata"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        tag_metadata: typing.Union[MetaOapg.properties.tag_metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'UpdateTag':
        return super().__new__(
            cls,
            *_args,
            description=description,
            tag_metadata=tag_metadata,
            _configuration=_configuration,
        )
