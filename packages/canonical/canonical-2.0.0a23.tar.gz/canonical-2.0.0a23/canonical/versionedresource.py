# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import ClassVar
from typing import Generic
from typing import Mapping
from typing import TypeVar

import pydantic

from .protocols import IRepository
from .objectmeta import ObjectMeta


__all__: list[str] = [
    'VersionedResource'
]

L = TypeVar('L')
S = TypeVar('S', bound=pydantic.BaseModel)
T = TypeVar('T', bound='VersionedResource[Any]')
V = TypeVar('V')
NOT_PROVIDED: object = object()


class VersionedResource(pydantic.BaseModel, Generic[S]):
    model_config = {'populate_by_name': True}
    version: ClassVar[str] = 'v1'
    _storage: IRepository['VersionedResource[S]'] = pydantic.PrivateAttr()

    api_version: str = pydantic.Field(
        default=...,
        alias='apiVersion',
        title="API Version",
        description=(
            "The `apiVersion` field defines the versioned schema of this "
            "representation of an object. Servers should convert recognized "
            "schemas to the latest internal value, and may reject "
            "unrecognized values."
        )
    )

    kind: str = pydantic.Field(
        default=...
    )

    metadata: ObjectMeta = pydantic.Field(
        default=...,
        description=(
            "`ObjectMeta` is metadata that all persisted resources "
            "must have, which includes all objects users must create."
        )
    )

    spec: S = pydantic.Field(
        default=...
    )

    @property
    def pk(self) -> Any:
        return self.get_primary_key()

    @classmethod
    def new(
        cls: type[T],
        name: str,
        spec: Mapping[str, Any],
        labels: Mapping[str, Any] | None = None
    ) -> T:
        metadata: Mapping[str, Any] = {
            'name': name,
            'labels': labels or {}
        }
        params: Mapping[str, Any] = {
            'api_version': cls.version,
            'kind': cls.__name__,
            'metadata': metadata,
            'spec': spec
        }
        return cls.model_validate(params)

    def attach(self, repo: IRepository[Any]):
        self._storage = repo
        return self

    def clone(self, **spec: Any):
        cloned = self.model_validate({
            **self.model_dump(),
            'spec': {**self.spec.model_dump(), **spec}
        })
        cloned.set_label('cloned', True)
        return cloned

    def get_label(self, name: str, factory: Callable[[Any], L] = str) -> L | None:
        value = self.metadata.labels.get(name)
        if value is None:
            return None
        return factory(value)

    def get_primary_key(self) -> Any:
        raise NotImplementedError

    def set_label(self, name: str, value: Any) -> Any | None:
        if value != NOT_PROVIDED:
            self.metadata.labels[name] = value
        return self.metadata.labels[name]

    def is_cloned(self) -> bool:
        return bool(self.get_label('cloned', bool))

    async def persist(self):
        await self._storage.persist(self)
        return self