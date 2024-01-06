# File generated from our OpenAPI spec by Stainless.

from __future__ import annotations

from .parent import Parent, AsyncParent, ParentWithRawResponse, AsyncParentWithRawResponse
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .parent.parent import Parent, AsyncParent

__all__ = ["ResourceRefs", "AsyncResourceRefs"]


class ResourceRefs(SyncAPIResource):
    @cached_property
    def parent(self) -> Parent:
        return Parent(self._client)

    @cached_property
    def with_raw_response(self) -> ResourceRefsWithRawResponse:
        return ResourceRefsWithRawResponse(self)


class AsyncResourceRefs(AsyncAPIResource):
    @cached_property
    def parent(self) -> AsyncParent:
        return AsyncParent(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncResourceRefsWithRawResponse:
        return AsyncResourceRefsWithRawResponse(self)


class ResourceRefsWithRawResponse:
    def __init__(self, resource_refs: ResourceRefs) -> None:
        self.parent = ParentWithRawResponse(resource_refs.parent)


class AsyncResourceRefsWithRawResponse:
    def __init__(self, resource_refs: AsyncResourceRefs) -> None:
        self.parent = AsyncParentWithRawResponse(resource_refs.parent)
