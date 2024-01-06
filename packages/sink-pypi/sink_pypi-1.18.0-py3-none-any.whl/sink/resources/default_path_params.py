# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from ..types import DefaultPathParamOnlyGlobalResponse, DefaultPathParamGlobalWithStandardResponse
from .._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NotGiven,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from .._base_client import (
    make_request_options,
)

__all__ = ["DefaultPathParams", "AsyncDefaultPathParams"]


class DefaultPathParams(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DefaultPathParamsWithRawResponse:
        return DefaultPathParamsWithRawResponse(self)

    def global_with_standard(
        self,
        id: str,
        *,
        camel_cased_path: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DefaultPathParamGlobalWithStandardResponse:
        """
        The operation takes a path param that is able to be set at the client level
        alongside a standard path param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if camel_cased_path is None:
            camel_cased_path = self._client._get_camel_case_path_param()

        return self._post(
            f"/default_path_params/path_params/{camel_cased_path}/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DefaultPathParamGlobalWithStandardResponse,
        )

    def only_global(
        self,
        *,
        client_path_param: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DefaultPathParamOnlyGlobalResponse:
        """
        The operation takes a path param that is able to be set at the client level.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if client_path_param is None:
            client_path_param = self._client._get_client_path_param_param()

        return self._post(
            f"/default_path_params/path_params/{client_path_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DefaultPathParamOnlyGlobalResponse,
        )


class AsyncDefaultPathParams(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDefaultPathParamsWithRawResponse:
        return AsyncDefaultPathParamsWithRawResponse(self)

    async def global_with_standard(
        self,
        id: str,
        *,
        camel_cased_path: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DefaultPathParamGlobalWithStandardResponse:
        """
        The operation takes a path param that is able to be set at the client level
        alongside a standard path param.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if camel_cased_path is None:
            camel_cased_path = self._client._get_camel_case_path_param()

        return await self._post(
            f"/default_path_params/path_params/{camel_cased_path}/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DefaultPathParamGlobalWithStandardResponse,
        )

    async def only_global(
        self,
        *,
        client_path_param: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DefaultPathParamOnlyGlobalResponse:
        """
        The operation takes a path param that is able to be set at the client level.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if client_path_param is None:
            client_path_param = self._client._get_client_path_param_param()

        return await self._post(
            f"/default_path_params/path_params/{client_path_param}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DefaultPathParamOnlyGlobalResponse,
        )


class DefaultPathParamsWithRawResponse:
    def __init__(self, default_path_params: DefaultPathParams) -> None:
        self.global_with_standard = to_raw_response_wrapper(
            default_path_params.global_with_standard,
        )
        self.only_global = to_raw_response_wrapper(
            default_path_params.only_global,
        )


class AsyncDefaultPathParamsWithRawResponse:
    def __init__(self, default_path_params: AsyncDefaultPathParams) -> None:
        self.global_with_standard = async_to_raw_response_wrapper(
            default_path_params.global_with_standard,
        )
        self.only_global = async_to_raw_response_wrapper(
            default_path_params.only_global,
        )
