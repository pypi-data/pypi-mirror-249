# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

import httpx

from .....types import Card
from ....._types import (
    NOT_GIVEN,
    Body,
    Query,
    Headers,
    NotGiven,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from ....._base_client import (
    make_request_options,
)

__all__ = ["LevelThree", "AsyncLevelThree"]


class LevelThree(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LevelThreeWithRawResponse:
        return LevelThreeWithRawResponse(self)

    def method_level_3(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class AsyncLevelThree(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLevelThreeWithRawResponse:
        return AsyncLevelThreeWithRawResponse(self)

    async def method_level_3(
        self,
        card_token: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Card:
        """
        Get card configuration such as spend limit and state.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/cards/{card_token}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Card,
        )


class LevelThreeWithRawResponse:
    def __init__(self, level_three: LevelThree) -> None:
        self.method_level_3 = to_raw_response_wrapper(
            level_three.method_level_3,
        )


class AsyncLevelThreeWithRawResponse:
    def __init__(self, level_three: AsyncLevelThree) -> None:
        self.method_level_3 = async_to_raw_response_wrapper(
            level_three.method_level_3,
        )
