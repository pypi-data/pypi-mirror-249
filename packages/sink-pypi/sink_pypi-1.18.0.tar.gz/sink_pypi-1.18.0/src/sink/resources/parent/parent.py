# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .child import Child, AsyncChild, ChildWithRawResponse, AsyncChildWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["Parent", "AsyncParent"]


class Parent(SyncAPIResource):
    @cached_property
    def child(self) -> Child:
        return Child(self._client)

    @cached_property
    def with_raw_response(self) -> ParentWithRawResponse:
        return ParentWithRawResponse(self)


class AsyncParent(AsyncAPIResource):
    @cached_property
    def child(self) -> AsyncChild:
        return AsyncChild(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncParentWithRawResponse:
        return AsyncParentWithRawResponse(self)


class ParentWithRawResponse:
    def __init__(self, parent: Parent) -> None:
        self.child = ChildWithRawResponse(parent.child)


class AsyncParentWithRawResponse:
    def __init__(self, parent: AsyncParent) -> None:
        self.child = AsyncChildWithRawResponse(parent.child)
