# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .eeoc import EEOCResource, AsyncEEOCResource, EEOCResourceWithRawResponse, AsyncEEOCResourceWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Casing", "AsyncCasing"]


class Casing(SyncAPIResource):
    @cached_property
    def eeoc(self) -> EEOCResource:
        return EEOCResource(self._client)

    @cached_property
    def with_raw_response(self) -> CasingWithRawResponse:
        return CasingWithRawResponse(self)


class AsyncCasing(AsyncAPIResource):
    @cached_property
    def eeoc(self) -> AsyncEEOCResource:
        return AsyncEEOCResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCasingWithRawResponse:
        return AsyncCasingWithRawResponse(self)


class CasingWithRawResponse:
    def __init__(self, casing: Casing) -> None:
        self.eeoc = EEOCResourceWithRawResponse(casing.eeoc)


class AsyncCasingWithRawResponse:
    def __init__(self, casing: AsyncCasing) -> None:
        self.eeoc = AsyncEEOCResourceWithRawResponse(casing.eeoc)
