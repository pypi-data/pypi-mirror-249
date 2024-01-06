# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from typing import List, Union
from datetime import date, datetime

import httpx

from .enums import Enums, AsyncEnums, EnumsWithRawResponse, AsyncEnumsWithRawResponse
from .arrays import Arrays, AsyncArrays, ArraysWithRawResponse, AsyncArraysWithRawResponse
from ...types import TypeDatesResponse, TypeDatetimesResponse, type_dates_params, type_datetimes_params
from .objects import Objects, AsyncObjects, ObjectsWithRawResponse, AsyncObjectsWithRawResponse
from ..._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NotGiven,
)
from ..._utils import maybe_transform
from ..._compat import cached_property
from .primitives import Primitives, AsyncPrimitives, PrimitivesWithRawResponse, AsyncPrimitivesWithRawResponse
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ..._base_client import (
    make_request_options,
)
from .read_only_params import (
    ReadOnlyParams,
    AsyncReadOnlyParams,
    ReadOnlyParamsWithRawResponse,
    AsyncReadOnlyParamsWithRawResponse,
)
from .write_only_responses import (
    WriteOnlyResponses,
    AsyncWriteOnlyResponses,
    WriteOnlyResponsesWithRawResponse,
    AsyncWriteOnlyResponsesWithRawResponse,
)

__all__ = ["Types", "AsyncTypes"]


class Types(SyncAPIResource):
    @cached_property
    def primitives(self) -> Primitives:
        return Primitives(self._client)

    @cached_property
    def read_only_params(self) -> ReadOnlyParams:
        return ReadOnlyParams(self._client)

    @cached_property
    def write_only_responses(self) -> WriteOnlyResponses:
        return WriteOnlyResponses(self._client)

    @cached_property
    def enums(self) -> Enums:
        return Enums(self._client)

    @cached_property
    def objects(self) -> Objects:
        return Objects(self._client)

    @cached_property
    def arrays(self) -> Arrays:
        return Arrays(self._client)

    @cached_property
    def with_raw_response(self) -> TypesWithRawResponse:
        return TypesWithRawResponse(self)

    def dates(
        self,
        *,
        required_date: Union[str, date],
        required_nullable_date: Union[str, date, None],
        list_date: List[Union[str, date]] | NotGiven = NOT_GIVEN,
        oneof_date: Union[Union[str, date], int] | NotGiven = NOT_GIVEN,
        optional_date: Union[str, date] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> TypeDatesResponse:
        """
        Endpoint that has date types should generate params/responses with rich date
        types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/dates",
            body=maybe_transform(
                {
                    "required_date": required_date,
                    "required_nullable_date": required_nullable_date,
                    "list_date": list_date,
                    "oneof_date": oneof_date,
                    "optional_date": optional_date,
                },
                type_dates_params.TypeDatesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatesResponse,
        )

    def datetimes(
        self,
        *,
        required_datetime: Union[str, datetime],
        required_nullable_datetime: Union[str, datetime, None],
        list_datetime: List[Union[str, datetime]] | NotGiven = NOT_GIVEN,
        oneof_datetime: Union[Union[str, datetime], int] | NotGiven = NOT_GIVEN,
        optional_datetime: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> TypeDatetimesResponse:
        """
        Endpoint that has date-time types.

        Args:
          oneof_datetime: union type coming from the `oneof_datetime` property

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/types/datetimes",
            body=maybe_transform(
                {
                    "required_datetime": required_datetime,
                    "required_nullable_datetime": required_nullable_datetime,
                    "list_datetime": list_datetime,
                    "oneof_datetime": oneof_datetime,
                    "optional_datetime": optional_datetime,
                },
                type_datetimes_params.TypeDatetimesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatetimesResponse,
        )


class AsyncTypes(AsyncAPIResource):
    @cached_property
    def primitives(self) -> AsyncPrimitives:
        return AsyncPrimitives(self._client)

    @cached_property
    def read_only_params(self) -> AsyncReadOnlyParams:
        return AsyncReadOnlyParams(self._client)

    @cached_property
    def write_only_responses(self) -> AsyncWriteOnlyResponses:
        return AsyncWriteOnlyResponses(self._client)

    @cached_property
    def enums(self) -> AsyncEnums:
        return AsyncEnums(self._client)

    @cached_property
    def objects(self) -> AsyncObjects:
        return AsyncObjects(self._client)

    @cached_property
    def arrays(self) -> AsyncArrays:
        return AsyncArrays(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTypesWithRawResponse:
        return AsyncTypesWithRawResponse(self)

    async def dates(
        self,
        *,
        required_date: Union[str, date],
        required_nullable_date: Union[str, date, None],
        list_date: List[Union[str, date]] | NotGiven = NOT_GIVEN,
        oneof_date: Union[Union[str, date], int] | NotGiven = NOT_GIVEN,
        optional_date: Union[str, date] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> TypeDatesResponse:
        """
        Endpoint that has date types should generate params/responses with rich date
        types.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/dates",
            body=maybe_transform(
                {
                    "required_date": required_date,
                    "required_nullable_date": required_nullable_date,
                    "list_date": list_date,
                    "oneof_date": oneof_date,
                    "optional_date": optional_date,
                },
                type_dates_params.TypeDatesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatesResponse,
        )

    async def datetimes(
        self,
        *,
        required_datetime: Union[str, datetime],
        required_nullable_datetime: Union[str, datetime, None],
        list_datetime: List[Union[str, datetime]] | NotGiven = NOT_GIVEN,
        oneof_datetime: Union[Union[str, datetime], int] | NotGiven = NOT_GIVEN,
        optional_datetime: Union[str, datetime] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> TypeDatetimesResponse:
        """
        Endpoint that has date-time types.

        Args:
          oneof_datetime: union type coming from the `oneof_datetime` property

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/types/datetimes",
            body=maybe_transform(
                {
                    "required_datetime": required_datetime,
                    "required_nullable_datetime": required_nullable_datetime,
                    "list_datetime": list_datetime,
                    "oneof_datetime": oneof_datetime,
                    "optional_datetime": optional_datetime,
                },
                type_datetimes_params.TypeDatetimesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TypeDatetimesResponse,
        )


class TypesWithRawResponse:
    def __init__(self, types: Types) -> None:
        self.primitives = PrimitivesWithRawResponse(types.primitives)
        self.read_only_params = ReadOnlyParamsWithRawResponse(types.read_only_params)
        self.write_only_responses = WriteOnlyResponsesWithRawResponse(types.write_only_responses)
        self.enums = EnumsWithRawResponse(types.enums)
        self.objects = ObjectsWithRawResponse(types.objects)
        self.arrays = ArraysWithRawResponse(types.arrays)

        self.dates = to_raw_response_wrapper(
            types.dates,
        )
        self.datetimes = to_raw_response_wrapper(
            types.datetimes,
        )


class AsyncTypesWithRawResponse:
    def __init__(self, types: AsyncTypes) -> None:
        self.primitives = AsyncPrimitivesWithRawResponse(types.primitives)
        self.read_only_params = AsyncReadOnlyParamsWithRawResponse(types.read_only_params)
        self.write_only_responses = AsyncWriteOnlyResponsesWithRawResponse(types.write_only_responses)
        self.enums = AsyncEnumsWithRawResponse(types.enums)
        self.objects = AsyncObjectsWithRawResponse(types.objects)
        self.arrays = AsyncArraysWithRawResponse(types.arrays)

        self.dates = async_to_raw_response_wrapper(
            types.dates,
        )
        self.datetimes = async_to_raw_response_wrapper(
            types.datetimes,
        )
