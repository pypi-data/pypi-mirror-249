# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .refs import Refs, AsyncRefs, RefsWithRawResponse, AsyncRefsWithRawResponse
from .cursor import Cursor, AsyncCursor, CursorWithRawResponse, AsyncCursorWithRawResponse
from .offset import Offset, AsyncOffset, OffsetWithRawResponse, AsyncOffsetWithRawResponse
from ..._compat import cached_property
from .cursor_id import CursorID, AsyncCursorID, CursorIDWithRawResponse, AsyncCursorIDWithRawResponse
from .fake_pages import FakePages, AsyncFakePages, FakePagesWithRawResponse, AsyncFakePagesWithRawResponse
from ..._resource import SyncAPIResource, AsyncAPIResource
from .page_number import PageNumber, AsyncPageNumber, PageNumberWithRawResponse, AsyncPageNumberWithRawResponse
from .response_headers import (
    ResponseHeaders,
    AsyncResponseHeaders,
    ResponseHeadersWithRawResponse,
    AsyncResponseHeadersWithRawResponse,
)
from .top_level_arrays import (
    TopLevelArrays,
    AsyncTopLevelArrays,
    TopLevelArraysWithRawResponse,
    AsyncTopLevelArraysWithRawResponse,
)

__all__ = ["PaginationTests", "AsyncPaginationTests"]


class PaginationTests(SyncAPIResource):
    @cached_property
    def page_number(self) -> PageNumber:
        return PageNumber(self._client)

    @cached_property
    def refs(self) -> Refs:
        return Refs(self._client)

    @cached_property
    def response_headers(self) -> ResponseHeaders:
        return ResponseHeaders(self._client)

    @cached_property
    def top_level_arrays(self) -> TopLevelArrays:
        return TopLevelArrays(self._client)

    @cached_property
    def cursor(self) -> Cursor:
        return Cursor(self._client)

    @cached_property
    def cursor_id(self) -> CursorID:
        return CursorID(self._client)

    @cached_property
    def offset(self) -> Offset:
        return Offset(self._client)

    @cached_property
    def fake_pages(self) -> FakePages:
        return FakePages(self._client)

    @cached_property
    def with_raw_response(self) -> PaginationTestsWithRawResponse:
        return PaginationTestsWithRawResponse(self)


class AsyncPaginationTests(AsyncAPIResource):
    @cached_property
    def page_number(self) -> AsyncPageNumber:
        return AsyncPageNumber(self._client)

    @cached_property
    def refs(self) -> AsyncRefs:
        return AsyncRefs(self._client)

    @cached_property
    def response_headers(self) -> AsyncResponseHeaders:
        return AsyncResponseHeaders(self._client)

    @cached_property
    def top_level_arrays(self) -> AsyncTopLevelArrays:
        return AsyncTopLevelArrays(self._client)

    @cached_property
    def cursor(self) -> AsyncCursor:
        return AsyncCursor(self._client)

    @cached_property
    def cursor_id(self) -> AsyncCursorID:
        return AsyncCursorID(self._client)

    @cached_property
    def offset(self) -> AsyncOffset:
        return AsyncOffset(self._client)

    @cached_property
    def fake_pages(self) -> AsyncFakePages:
        return AsyncFakePages(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPaginationTestsWithRawResponse:
        return AsyncPaginationTestsWithRawResponse(self)


class PaginationTestsWithRawResponse:
    def __init__(self, pagination_tests: PaginationTests) -> None:
        self.page_number = PageNumberWithRawResponse(pagination_tests.page_number)
        self.refs = RefsWithRawResponse(pagination_tests.refs)
        self.response_headers = ResponseHeadersWithRawResponse(pagination_tests.response_headers)
        self.top_level_arrays = TopLevelArraysWithRawResponse(pagination_tests.top_level_arrays)
        self.cursor = CursorWithRawResponse(pagination_tests.cursor)
        self.cursor_id = CursorIDWithRawResponse(pagination_tests.cursor_id)
        self.offset = OffsetWithRawResponse(pagination_tests.offset)
        self.fake_pages = FakePagesWithRawResponse(pagination_tests.fake_pages)


class AsyncPaginationTestsWithRawResponse:
    def __init__(self, pagination_tests: AsyncPaginationTests) -> None:
        self.page_number = AsyncPageNumberWithRawResponse(pagination_tests.page_number)
        self.refs = AsyncRefsWithRawResponse(pagination_tests.refs)
        self.response_headers = AsyncResponseHeadersWithRawResponse(pagination_tests.response_headers)
        self.top_level_arrays = AsyncTopLevelArraysWithRawResponse(pagination_tests.top_level_arrays)
        self.cursor = AsyncCursorWithRawResponse(pagination_tests.cursor)
        self.cursor_id = AsyncCursorIDWithRawResponse(pagination_tests.cursor_id)
        self.offset = AsyncOffsetWithRawResponse(pagination_tests.offset)
        self.fake_pages = AsyncFakePagesWithRawResponse(pagination_tests.fake_pages)
