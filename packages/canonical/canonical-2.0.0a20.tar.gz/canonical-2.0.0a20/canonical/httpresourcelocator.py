# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import urllib.parse
from typing import Any

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema

from .stringrepresentable import StringRepresentable


class HTTPResourceLocator(StringRepresentable):

    @classmethod
    def __get_pydantic_core_schema__(cls, *_: Any) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(max_length=2048),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(cls),
                core_schema.chain_schema([
                    core_schema.no_info_plain_validator_function(str),
                    core_schema.str_schema(max_length=2048),
                    core_schema.no_info_plain_validator_function(cls.fromstring)
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue: # pragma: no cover
        return handler(core_schema.str_schema(max_length=2048))

    @classmethod
    def fromstring(cls, v: str, _: Any = None):
        p = urllib.parse.urlparse(v)
        if p.scheme not in {'http', 'https'}:
            raise ValueError(f"Not a valid URL: {v[:128]}")
        return cls(v)

    def __init__(self, value: str):
        self.__value = value
        
    def __str__(self) -> str:  # pragma: no cover
        return self.__value