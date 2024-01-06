# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from .import_ import (
    ImportResource,
    AsyncImportResource,
    ImportResourceWithRawResponse,
    AsyncImportResourceWithRawResponse,
)
from .methods import Methods, AsyncMethods, MethodsWithRawResponse, AsyncMethodsWithRawResponse
from ...._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NoneType,
    NotGiven,
)
from ...._utils import maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ....types.names import reserved_name_common_reserved_params_params
from ...._base_client import (
    make_request_options,
)

__all__ = ["ReservedNames", "AsyncReservedNames"]


class ReservedNames(SyncAPIResource):
    @cached_property
    def import_(self) -> ImportResource:
        return ImportResource(self._client)

    @cached_property
    def methods(self) -> Methods:
        return Methods(self._client)

    @cached_property
    def with_raw_response(self) -> ReservedNamesWithRawResponse:
        return ReservedNamesWithRawResponse(self)

    def common_reserved_params(
        self,
        *,
        from_: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property name that can conflict with
        language keywords.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/names/reserved_names/common_reserved_params",
            body=maybe_transform(
                {"from_": from_}, reserved_name_common_reserved_params_params.ReservedNameCommonReservedParamsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class AsyncReservedNames(AsyncAPIResource):
    @cached_property
    def import_(self) -> AsyncImportResource:
        return AsyncImportResource(self._client)

    @cached_property
    def methods(self) -> AsyncMethods:
        return AsyncMethods(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncReservedNamesWithRawResponse:
        return AsyncReservedNamesWithRawResponse(self)

    async def common_reserved_params(
        self,
        *,
        from_: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> None:
        """
        Endpoint with a `requestBody` that has a property name that can conflict with
        language keywords.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/names/reserved_names/common_reserved_params",
            body=maybe_transform(
                {"from_": from_}, reserved_name_common_reserved_params_params.ReservedNameCommonReservedParamsParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=NoneType,
        )


class ReservedNamesWithRawResponse:
    def __init__(self, reserved_names: ReservedNames) -> None:
        self.import_ = ImportResourceWithRawResponse(reserved_names.import_)
        self.methods = MethodsWithRawResponse(reserved_names.methods)

        self.common_reserved_params = to_raw_response_wrapper(
            reserved_names.common_reserved_params,
        )


class AsyncReservedNamesWithRawResponse:
    def __init__(self, reserved_names: AsyncReservedNames) -> None:
        self.import_ = AsyncImportResourceWithRawResponse(reserved_names.import_)
        self.methods = AsyncMethodsWithRawResponse(reserved_names.methods)

        self.common_reserved_params = async_to_raw_response_wrapper(
            reserved_names.common_reserved_params,
        )
