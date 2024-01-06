# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from ..._compat import cached_property
from .level_one import LevelOne, AsyncLevelOne, LevelOneWithRawResponse, AsyncLevelOneWithRawResponse
from ..._resource import SyncAPIResource, AsyncAPIResource
from .level_one.level_one import LevelOne, AsyncLevelOne

__all__ = ["DeeplyNested", "AsyncDeeplyNested"]


class DeeplyNested(SyncAPIResource):
    @cached_property
    def level_one(self) -> LevelOne:
        return LevelOne(self._client)

    @cached_property
    def with_raw_response(self) -> DeeplyNestedWithRawResponse:
        return DeeplyNestedWithRawResponse(self)


class AsyncDeeplyNested(AsyncAPIResource):
    @cached_property
    def level_one(self) -> AsyncLevelOne:
        return AsyncLevelOne(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDeeplyNestedWithRawResponse:
        return AsyncDeeplyNestedWithRawResponse(self)


class DeeplyNestedWithRawResponse:
    def __init__(self, deeply_nested: DeeplyNested) -> None:
        self.level_one = LevelOneWithRawResponse(deeply_nested.level_one)


class AsyncDeeplyNestedWithRawResponse:
    def __init__(self, deeply_nested: AsyncDeeplyNested) -> None:
        self.level_one = AsyncLevelOneWithRawResponse(deeply_nested.level_one)
