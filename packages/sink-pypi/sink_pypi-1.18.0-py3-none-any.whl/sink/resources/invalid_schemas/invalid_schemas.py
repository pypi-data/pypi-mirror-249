# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .arrays import Arrays, AsyncArrays, ArraysWithRawResponse, AsyncArraysWithRawResponse
from .objects import Objects, AsyncObjects, ObjectsWithRawResponse, AsyncObjectsWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["InvalidSchemas", "AsyncInvalidSchemas"]


class InvalidSchemas(SyncAPIResource):
    @cached_property
    def arrays(self) -> Arrays:
        return Arrays(self._client)

    @cached_property
    def objects(self) -> Objects:
        return Objects(self._client)

    @cached_property
    def with_raw_response(self) -> InvalidSchemasWithRawResponse:
        return InvalidSchemasWithRawResponse(self)


class AsyncInvalidSchemas(AsyncAPIResource):
    @cached_property
    def arrays(self) -> AsyncArrays:
        return AsyncArrays(self._client)

    @cached_property
    def objects(self) -> AsyncObjects:
        return AsyncObjects(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncInvalidSchemasWithRawResponse:
        return AsyncInvalidSchemasWithRawResponse(self)


class InvalidSchemasWithRawResponse:
    def __init__(self, invalid_schemas: InvalidSchemas) -> None:
        self.arrays = ArraysWithRawResponse(invalid_schemas.arrays)
        self.objects = ObjectsWithRawResponse(invalid_schemas.objects)


class AsyncInvalidSchemasWithRawResponse:
    def __init__(self, invalid_schemas: AsyncInvalidSchemas) -> None:
        self.arrays = AsyncArraysWithRawResponse(invalid_schemas.arrays)
        self.objects = AsyncObjectsWithRawResponse(invalid_schemas.objects)
