# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .shared_responses import (
    SharedResponses,
    AsyncSharedResponses,
    SharedResponsesWithRawResponse,
    AsyncSharedResponsesWithRawResponse,
)

__all__ = ["Recursion", "AsyncRecursion"]


class Recursion(SyncAPIResource):
    @cached_property
    def shared_responses(self) -> SharedResponses:
        return SharedResponses(self._client)

    @cached_property
    def with_raw_response(self) -> RecursionWithRawResponse:
        return RecursionWithRawResponse(self)


class AsyncRecursion(AsyncAPIResource):
    @cached_property
    def shared_responses(self) -> AsyncSharedResponses:
        return AsyncSharedResponses(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRecursionWithRawResponse:
        return AsyncRecursionWithRawResponse(self)


class RecursionWithRawResponse:
    def __init__(self, recursion: Recursion) -> None:
        self.shared_responses = SharedResponsesWithRawResponse(recursion.shared_responses)


class AsyncRecursionWithRawResponse:
    def __init__(self, recursion: AsyncRecursion) -> None:
        self.shared_responses = AsyncSharedResponsesWithRawResponse(recursion.shared_responses)
