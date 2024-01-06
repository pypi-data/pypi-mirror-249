# File generated from our OpenAPI spec by Stainless.

from typing import Any, List, Type, Generic, Mapping, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

import httpx
from httpx import Response

from ._types import ModelT
from ._utils import is_mapping
from ._models import BaseModel
from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage
from .types.shared import PageCursorSharedRefPagination

__all__ = [
    "SyncPageCursor",
    "AsyncPageCursor",
    "SyncPageCursorFromHeaders",
    "AsyncPageCursorFromHeaders",
    "SyncPageCursorTopLevelArray",
    "AsyncPageCursorTopLevelArray",
    "SyncPageCursorSharedRef",
    "AsyncPageCursorSharedRef",
    "PageCursorNestedObjectRefObjectProp",
    "SyncPageCursorNestedObjectRef",
    "AsyncPageCursorNestedObjectRef",
    "SyncPagePageNumber",
    "AsyncPagePageNumber",
    "SyncPageOffsetTotalCount",
    "AsyncPageOffsetTotalCount",
    "SyncPageOffset",
    "AsyncPageOffset",
    "SyncPageCursorURL",
    "AsyncPageCursorURL",
    "SyncPageCursorID",
    "AsyncPageCursorID",
    "SyncFakePage",
    "AsyncFakePage",
]

_BaseModelT = TypeVar("_BaseModelT", bound=BaseModel)


@runtime_checkable
class PageCursorIDItem(Protocol):
    id: Optional[str]


class SyncPageCursor(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursor(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = self.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class SyncPageCursorFromHeaders(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class AsyncPageCursorFromHeaders(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class SyncPageCursorTopLevelArray(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"data": data}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class AsyncPageCursorTopLevelArray(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    my_cursor: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        my_cursor = self.my_cursor
        if not my_cursor:
            return None

        return PageInfo(params={"cursor": my_cursor})

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"data": data}),
                "my_cursor": response.headers.get("X-My-Cursor"),
            },
        )


class SyncPageCursorSharedRef(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    pagination: Optional[PageCursorSharedRefPagination] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = None
        if self.pagination is not None:
            cursor = self.pagination.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class AsyncPageCursorSharedRef(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    pagination: Optional[PageCursorSharedRefPagination] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        cursor = None
        if self.pagination is not None:
            cursor = self.pagination.cursor
        if not cursor:
            return None

        return PageInfo(params={"cursor": cursor})


class PageCursorNestedObjectRefObjectProp(BaseModel):
    foo: Optional[str] = None


class SyncPageCursorNestedObjectRef(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    nested_object_cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedObjectRefObjectProp] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        nested_object_cursor = self.nested_object_cursor
        if not nested_object_cursor:
            return None

        return PageInfo(params={"cursor": nested_object_cursor})


class AsyncPageCursorNestedObjectRef(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    nested_object_cursor: Optional[str] = None
    object_prop: Optional[PageCursorNestedObjectRefObjectProp] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        nested_object_cursor = self.nested_object_cursor
        if not nested_object_cursor:
            return None

        return PageInfo(params={"cursor": nested_object_cursor})


class SyncPagePageNumber(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    page: Optional[int] = None
    last_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        last_page = cast("int | None", self._options.params.get("page"))
        if last_page is not None and current_page <= last_page:
            # The API didn't return a new page in the last request
            return None

        return PageInfo(params={"page": current_page + 1})


class AsyncPagePageNumber(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    page: Optional[int] = None
    last_page: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        current_page = self.page
        if current_page is None:
            current_page = 1

        last_page = cast("int | None", self._options.params.get("page"))
        if last_page is not None and current_page <= last_page:
            # The API didn't return a new page in the last request
            return None

        return PageInfo(params={"page": current_page + 1})


class SyncPageOffsetTotalCount(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    total_count: Optional[int] = None
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None

        length = len(self._get_page_items())
        current_count = offset + length

        total_count = self.total_count
        if total_count is None:
            return None

        if current_count < total_count:
            return PageInfo(params={"offset": current_count})

        return None


class AsyncPageOffsetTotalCount(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    total_count: Optional[int] = None
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None

        length = len(self._get_page_items())
        current_count = offset + length

        total_count = self.total_count
        if total_count is None:
            return None

        if current_count < total_count:
            return PageInfo(params={"offset": current_count})

        return None


class SyncPageOffset(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class AsyncPageOffset(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    offset: Optional[int] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        offset = self.offset
        if offset is None:
            return None

        length = len(self._get_page_items())
        current_count = offset + length

        return PageInfo(params={"offset": current_count})


class SyncPageCursorURL(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    next_page: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = self.next_page
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))


class AsyncPageCursorURL(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]
    next_page: Optional[str] = None

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        url = self.next_page
        if url is None:
            return None

        return PageInfo(url=httpx.URL(url))


class SyncPageCursorID(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        data = self.data
        if not data:
            return None

        item = cast(Any, data[-1])
        if not isinstance(item, PageCursorIDItem) or item.id is None:
            # TODO emit warning log
            return None

        return PageInfo(params={"next_id": item.id})


class AsyncPageCursorID(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    data: List[ModelT]

    @override
    def _get_page_items(self) -> List[ModelT]:
        data = self.data
        if not data:
            return []
        return data

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        data = self.data
        if not data:
            return None

        item = cast(Any, data[-1])
        if not isinstance(item, PageCursorIDItem) or item.id is None:
            # TODO emit warning log
            return None

        return PageInfo(params={"next_id": item.id})


class SyncFakePage(BaseSyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    items: List[ModelT]

    @override
    def _get_page_items(self) -> List[ModelT]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )


class AsyncFakePage(BaseAsyncPage[ModelT], BasePage[ModelT], Generic[ModelT]):
    items: List[ModelT]

    @override
    def _get_page_items(self) -> List[ModelT]:
        items = self.items
        if not items:
            return []
        return items

    @override
    def next_page_info(self) -> None:
        """
        This page represents a response that isn't actually paginated at the API level
        so there will never be a next page.
        """
        return None

    @classmethod
    def build(cls: Type[_BaseModelT], *, response: Response, data: object) -> _BaseModelT:  # noqa: ARG003
        return cls.construct(
            None,
            **{
                **(cast(Mapping[str, Any], data) if is_mapping(data) else {"items": data}),
            },
        )
