# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .payments import Payments, AsyncPayments, PaymentsWithRawResponse, AsyncPaymentsWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["CompanyResource", "AsyncCompanyResource"]


class CompanyResource(SyncAPIResource):
    @cached_property
    def payments(self) -> Payments:
        return Payments(self._client)

    @cached_property
    def with_raw_response(self) -> CompanyResourceWithRawResponse:
        return CompanyResourceWithRawResponse(self)


class AsyncCompanyResource(AsyncAPIResource):
    @cached_property
    def payments(self) -> AsyncPayments:
        return AsyncPayments(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCompanyResourceWithRawResponse:
        return AsyncCompanyResourceWithRawResponse(self)


class CompanyResourceWithRawResponse:
    def __init__(self, company: CompanyResource) -> None:
        self.payments = PaymentsWithRawResponse(company.payments)


class AsyncCompanyResourceWithRawResponse:
    def __init__(self, company: AsyncCompanyResource) -> None:
        self.payments = AsyncPaymentsWithRawResponse(company.payments)
