# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ..types import binary_with_path_and_body_param_params
from .._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NotGiven,
)
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from .._base_client import (
    HttpxBinaryResponseContent,
    make_request_options,
)

__all__ = ["Binaries", "AsyncBinaries"]


class Binaries(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BinariesWithRawResponse:
        return BinariesWithRawResponse(self)

    def return_binary(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HttpxBinaryResponseContent:
        """Return a binary response."""
        return self._get(
            "/binaries/return_binary",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HttpxBinaryResponseContent,
        )

    def with_path_and_body_param(
        self,
        id: str,
        *,
        foo: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> HttpxBinaryResponseContent:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            f"/binaries/with_path_and_body_param/{id}",
            body=maybe_transform({"foo": foo}, binary_with_path_and_body_param_params.BinaryWithPathAndBodyParamParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=HttpxBinaryResponseContent,
        )

    def with_path_param(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HttpxBinaryResponseContent:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/binaries/with_path_param/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HttpxBinaryResponseContent,
        )


class AsyncBinaries(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBinariesWithRawResponse:
        return AsyncBinariesWithRawResponse(self)

    async def return_binary(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HttpxBinaryResponseContent:
        """Return a binary response."""
        return await self._get(
            "/binaries/return_binary",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HttpxBinaryResponseContent,
        )

    async def with_path_and_body_param(
        self,
        id: str,
        *,
        foo: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> HttpxBinaryResponseContent:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            f"/binaries/with_path_and_body_param/{id}",
            body=maybe_transform({"foo": foo}, binary_with_path_and_body_param_params.BinaryWithPathAndBodyParamParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=HttpxBinaryResponseContent,
        )

    async def with_path_param(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HttpxBinaryResponseContent:
        """
        Return a binary response.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/binaries/with_path_param/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HttpxBinaryResponseContent,
        )


class BinariesWithRawResponse:
    def __init__(self, binaries: Binaries) -> None:
        self.return_binary = to_raw_response_wrapper(
            binaries.return_binary,
        )
        self.with_path_and_body_param = to_raw_response_wrapper(
            binaries.with_path_and_body_param,
        )
        self.with_path_param = to_raw_response_wrapper(
            binaries.with_path_param,
        )


class AsyncBinariesWithRawResponse:
    def __init__(self, binaries: AsyncBinaries) -> None:
        self.return_binary = async_to_raw_response_wrapper(
            binaries.return_binary,
        )
        self.with_path_and_body_param = async_to_raw_response_wrapper(
            binaries.with_path_and_body_param,
        )
        self.with_path_param = async_to_raw_response_wrapper(
            binaries.with_path_param,
        )
