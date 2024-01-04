from __future__ import annotations

import functools
from typing import (
    Any,
    TypeVar,
    Generic,
    Callable,
    Self,
    overload,
)
from collections.abc import Callable, Iterable, Iterator

from _typeshed import Incomplete
from bs4 import BeautifulSoup
from bs4.formatter import Formatter, _EntitySubstitution
from bs4.element import Tag, _PageElementT, _Strainable, SoupStrainer, NavigableString, ResultSet, PageElement

from .utils import FullDunder

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)


class BroadcastList(list[T]):
    @property
    def bc(self) -> _BroadcastedList[T]:
        return _BroadcastedList(self)


class _BroadcastedList(FullDunder, Generic[T_co]):
    _broadcastlist_value: list

    def _callable_attr_broadcast(self, *args, **kwargs) -> BroadcastList:
        ...

    def __init__(self, broadcastlist: BroadcastList[T_co]) -> None:
        ...

    def __getattr__(self, __name: str) -> Callable[..., BroadcastList] | BroadcastList:
        ...

    def __setattr__(self, name: str, value) -> None:
        ...

    def __str__(self) -> str:
        ...

    __repr__ = __str__  # type: ignore

    def broadcast_str(self) -> BroadcastList[str]:
        ...

    def broadcast_repr(self) -> BroadcastList[str]:
        ...


class TagBroadcastList(BroadcastList[Tag]):
    @property
    def bc(self) -> _TagBroadcastedList:
        ...


class _TagBroadcastedList(_BroadcastedList[Tag]):
    """Chaining BroadcastED list especially for Tags."""
    parent: BroadcastList[Tag | None]
    previous_element: BroadcastList[PageElement | None]
    next_element: BroadcastList[PageElement | None]
    next_sibling: BroadcastList[PageElement | None]
    previous_sibling: BroadcastList[PageElement | None]
    def setup(
        self,
        parent: Tag | None = None,
        previous_element: PageElement | None = None,
        next_element: PageElement | None = None,
        previous_sibling: PageElement | None = None,
        next_sibling: PageElement | None = None,
    ) -> BroadcastList[None]: ...
    def format_string(self, s: str, formatter: Formatter | str | None) -> BroadcastList[str]: ...
    def formatter_for_name(self, formatter: Formatter | str | _EntitySubstitution) -> BroadcastList[None]: ...
    nextSibling: BroadcastList[PageElement | None]
    previousSibling: BroadcastList[PageElement | None]
    @property
    def stripped_strings(self) -> BroadcastList[Iterator[str]]: ...
    def get_text(self, separator: str = "", strip: bool = False, types: tuple[type[NavigableString], ...] = ...) -> BroadcastList[str]: ...
    getText = get_text
    @property
    def text(self) -> BroadcastList[str]: ...
    def replace_with(self, *args: PageElement | str) -> BroadcastList[Self]: ...
    replaceWith = replace_with
    def unwrap(self) -> BroadcastList[Self]: ...
    replace_with_children = unwrap
    replaceWithChildren = unwrap
    def wrap(self, wrap_inside: _PageElementT) -> BroadcastList[_PageElementT]: ...
    def extract(self, _self_index: int | None = None) -> BroadcastList[Self]: ...
    def Einsert(self, position: int, new_child: PageElement | str) -> BroadcastList[None]: ...
    def Eappend(self, tag: PageElement | str) -> BroadcastList[None]: ...
    def Eextend(self, tags: Iterable[PageElement | str]) -> BroadcastList[None]: ...
    def insert_before(self, *args: PageElement | str) -> BroadcastList[None]: ...
    def insert_after(self, *args: PageElement | str) -> BroadcastList[None]: ...
    def find_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | NavigableString | None]: ...
    findNext = find_next
    def find_all_next(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[PageElement]]: ...
    findAllNext = find_all_next
    def find_next_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | NavigableString | None]: ...
    findNextSibling = find_next_sibling
    def find_next_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[PageElement]]: ...
    findNextSiblings = find_next_siblings
    fetchNextSiblings = find_next_siblings
    def find_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | NavigableString | None]: ...
    findPrevious = find_previous
    def find_all_previous(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[PageElement]]: ...
    findAllPrevious = find_all_previous
    fetchPrevious = find_all_previous
    def find_previous_sibling(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | NavigableString | None]: ...
    findPreviousSibling = find_previous_sibling
    def find_previous_siblings(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[PageElement]]: ...
    findPreviousSiblings = find_previous_siblings
    fetchPreviousSiblings = find_previous_siblings
    def find_parent(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | None]: ...
    findParent = find_parent
    def find_parents(
        self,
        name: _Strainable | SoupStrainer | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[Tag]]: ...
    findParents = find_parents
    fetchParents = find_parents
    @property
    def next(self) -> BroadcastList[Tag | NavigableString | None]: ...
    @property
    def previous(self) -> BroadcastList[Tag | NavigableString | None]: ...
    @property
    def next_elements(self) -> BroadcastList[Iterable[PageElement]]: ...
    @property
    def next_siblings(self) -> BroadcastList[Iterable[PageElement]]: ...
    @property
    def previous_elements(self) -> BroadcastList[Iterable[PageElement]]: ...
    @property
    def previous_siblings(self) -> BroadcastList[Iterable[PageElement]]: ...
    @property
    def parents(self) -> BroadcastList[Iterable[Tag]]: ...
    @property
    def decomposed(self) -> BroadcastList[bool]: ...
    def nextGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def nextSiblingGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def previousGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def previousSiblingGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def parentGenerator(self) -> BroadcastList[Iterable[Tag]]: ...

    # TAGS

    parser_class: BroadcastList[type[BeautifulSoup] | None]
    name: BroadcastList[str]
    namespace: BroadcastList[str | None]
    prefix: BroadcastList[str | None]
    sourceline: BroadcastList[int | None]
    sourcepos: BroadcastList[int | None]
    known_xml: BroadcastList[bool | None]
    attrs: BroadcastList[dict[str, str]]
    contents: BroadcastList[list[PageElement]]
    hidden: BroadcastList[bool]
    can_be_empty_element: BroadcastList[bool | None]
    cdata_list_attributes: BroadcastList[list[str] | None]
    preserve_whitespace_tags: BroadcastList[list[str] | None]
    # def __init__(
    #     self,
    #     parser: BeautifulSoup | None = None,
    #     builder: TreeBuilder | None = None,
    #     name: str | None = None,
    #     namespace: str | None = None,
    #     prefix: str | None = None,
    #     attrs: dict[str, str] | None = None,
    #     parent: Tag | None = None,
    #     previous: PageElement | None = None,
    #     is_xml: bool | None = None,
    #     sourceline: int | None = None,
    #     sourcepos: int | None = None,
    #     can_be_empty_element: bool | None = None,
    #     cdata_list_attributes: list[str] | None = None,
    #     preserve_whitespace_tags: list[str] | None = None,
    #     interesting_string_types: type[NavigableString] | tuple[type[NavigableString], ...] | None = None,
    #     namespaces: dict[str, str] | None = None,
    # ) -> NewTagBroadcastList[None]: ...
    parserClass: BroadcastList[type[BeautifulSoup] | None]
    def __copy__(self) -> BroadcastList[Self]: ...
    @property
    def is_empty_element(self) -> BroadcastList[bool]: ...
    @property
    def isSelfClosing(self) -> BroadcastList[bool]: ...
    @property
    def string(self) -> BroadcastList[str | None]: ...
    @string.setter
    def string(self, string: str) -> BroadcastList[None]: ...
    DEFAULT_INTERESTING_STRING_TYPES: BroadcastList[tuple[type[NavigableString], ...]]
    @property
    def strings(self) -> BroadcastList[Iterable[str]]: ...
    def decompose(self) -> BroadcastList[None]: ...
    def Eclear(self, decompose: bool = False) -> BroadcastList[None]: ...
    def smooth(self) -> BroadcastList[None]: ...
    def Eindex(self, element: PageElement) -> BroadcastList[int]: ...
    def get(self, key: str, default: str | list[str] | None = None) -> BroadcastList[str | list[str] | None]: ...
    def get_attribute_list(self, key: str, default: str | list[str] | None = None) -> BroadcastList[list[str]]: ...
    def has_attr(self, key: str) -> BroadcastList[bool]: ...
    def __hash__(self) -> BroadcastList[int]: ...
    def __getitem__(self, key: str) -> BroadcastList[str | list[str]]: ...
    def __iter__(self) -> BroadcastList[Iterator[PageElement]]: ...
    def __len__(self) -> BroadcastList[int]: ...
    def __contains__(self, x: object) -> BroadcastList[bool]: ...
    def __bool__(self) -> BroadcastList[bool]: ...
    def __setitem__(self, key: str, value: str | list[str]) -> BroadcastList[None]: ...
    def __delitem__(self, key: str) -> BroadcastList[None]: ...
    def __getattr__(self, tag: str) -> BroadcastList[Tag | None]: ...
    def __eq__(self, other: object) -> BroadcastList[bool]: ...
    def __ne__(self, other: object) -> BroadcastList[bool]: ...
    def __unicode__(self) -> BroadcastList[str]: ...
    def encode(
        self,
        encoding: str = "utf-8",
        indent_level: int | None = None,
        formatter: str | Formatter = "minimal",
        errors: str = "xmlcharrefreplace",
    ) -> BroadcastList[bytes]: ...
    def decode(
        self,
        indent_level: int | None = None,
        eventual_encoding: str = "utf-8",
        formatter: str | Formatter = "minimal",
        iterator: Iterator[PageElement] | None = None,
    ) -> BroadcastList[str]: ...
    @overload
    def prettify(self, encoding: str, formatter: str | Formatter = "minimal") -> BroadcastList[bytes]: ...
    @overload
    def prettify(self, encoding: None = None, formatter: str | Formatter = "minimal") -> BroadcastList[str]: ...
    def decode_contents(
        self, indent_level: int | None = None, eventual_encoding: str = "utf-8", formatter: str | Formatter = "minimal"
    ) -> BroadcastList[str]: ...
    def encode_contents(
        self, indent_level: int | None = None, encoding: str = "utf-8", formatter: str | Formatter = "minimal"
    ) -> BroadcastList[bytes]: ...
    def renderContents(self, encoding: str = "utf-8", prettyPrint: bool = False, indentLevel: int = 0) -> BroadcastList[bytes]: ...
    def find(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[Tag | NavigableString | None]: ...
    findChild = find
    def find_all(
        self,
        name: _Strainable | None = None,
        attrs: dict[str, _Strainable] | _Strainable = {},
        recursive: bool = True,
        string: _Strainable | None = None,
        limit: int | None = None,
        **kwargs: _Strainable,
    ) -> BroadcastList[ResultSet[Any]]: ...
    __call__ = find_all
    findAll = find_all
    findChildren = find_all
    @property
    def children(self) -> BroadcastList[Iterable[PageElement]]: ...
    @property
    def descendants(self) -> BroadcastList[Iterable[PageElement]]: ...
    def select_one(
        self, selector: str, namespaces: Incomplete | None = None, *, flags: int = ..., custom: dict[str, str] | None = ...
    ) -> BroadcastList[Tag | None]: ...
    def select(
        self,
        selector: str,
        namespaces: Incomplete | None = None,
        limit: int | None = None,
        *,
        flags: int = ...,
        custom: dict[str, str] | None = ...,
    ) -> BroadcastList[ResultSet[Tag]]: ...
    def childGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def recursiveChildGenerator(self) -> BroadcastList[Iterable[PageElement]]: ...
    def has_key(self, key: str) -> BroadcastList[bool]: ...

