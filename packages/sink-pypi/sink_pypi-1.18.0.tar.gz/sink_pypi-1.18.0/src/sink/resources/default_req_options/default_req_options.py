# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from .child import Child, AsyncChild, ChildWithRawResponse, AsyncChildWithRawResponse
from ..._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NotGiven,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import (
    make_request_options,
)
from ...types.shared import BasicSharedModelObject

__all__ = ["DefaultReqOptions", "AsyncDefaultReqOptions"]


class DefaultReqOptions(SyncAPIResource):
    @cached_property
    def child(self) -> Child:
        return Child(self._client)

    @cached_property
    def with_raw_response(self) -> DefaultReqOptionsWithRawResponse:
        return DefaultReqOptionsWithRawResponse(self)

    def example_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BasicSharedModelObject:
        """Testing resource level default request options."""
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return self._get(
            "/default_req_options",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )


class AsyncDefaultReqOptions(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChild:
        return AsyncChild(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDefaultReqOptionsWithRawResponse:
        return AsyncDefaultReqOptionsWithRawResponse(self)

    async def example_method(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BasicSharedModelObject:
        """Testing resource level default request options."""
        extra_headers = {"X-My-Header": "true", "X-My-Other-Header": "false", **(extra_headers or {})}
        return await self._get(
            "/default_req_options",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BasicSharedModelObject,
        )


class DefaultReqOptionsWithRawResponse:
    def __init__(self, default_req_options: DefaultReqOptions) -> None:
        self.child = ChildWithRawResponse(default_req_options.child)

        self.example_method = to_raw_response_wrapper(
            default_req_options.example_method,
        )


class AsyncDefaultReqOptionsWithRawResponse:
    def __init__(self, default_req_options: AsyncDefaultReqOptions) -> None:
        self.child = AsyncChildWithRawResponse(default_req_options.child)

        self.example_method = async_to_raw_response_wrapper(
            default_req_options.example_method,
        )
