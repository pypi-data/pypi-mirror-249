from __future__ import annotations

import functools
import logging
from typing import (
    Any,
    Hashable,
    Mapping,
    Iterable,
    Callable,
)

from frozendict import frozendict


def made_it_hashable(value, alert: bool = True, error: bool = False) -> Any:
    if isinstance(value, Hashable):
        return value
    # 앞에서 Hashable은 이미 나가기 때문에 Iterable이나 Mapping 검사 시 hashable인지는 검사하지 않아도 됨.
    if isinstance(value, Mapping):  # Mapping은 Iterable이기 때문에 Iterable보다 더 먼저 와야 값이 손상되지 않음!
        return frozendict(value)
    if isinstance(value, Iterable):  # Mapping같이 특정한 경우에는 값이 손상될 수 있음.
        return tuple(value)
    if error:
        raise TypeError(f"type of '{value}' {type(value)}, "
                        "which is nether hashable, iterable(like list), nor mapping(like dict).")
    if alert:
        logging.warning(f"type of '{value}' {type(value)}, "
                        "which is nether hashable, iterable(like list), nor mapping(like dict). "
                        "So this thing will not be converted to hashable, that means this function "
                        "cannot be cached if your're using things like lru_cache.")
    return value


def freeze_dict_and_list(alert: bool = True, error: bool = False):
    """
    기본적으로는 가장 흔한 mutable인 mapping와 unhashable한 iterable를 hashable로 변환합니다.
    만악 dict와 list 외의 mutable이 있다면 아무런 변환 없이 넘깁니다.
    이때 alert가 True라면 경고를 내보내고, error가 True이면 exception이 나갑니다.
    """
    def wrapper(func: Callable):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            # 속도를 위해 제너레이터 컴프리헨션 대신 리스트 > 튜플 변환 사용 (약 1.5~2배 가량 빠름)
            new_args = [made_it_hashable(argument, alert, error) for argument in args]
            new_kwargs = {kwname: made_it_hashable(kwvalue)
                          for kwname, kwvalue in kwargs.items()}
            logging.debug((new_args, new_kwargs))
            return func(*new_args, **new_kwargs)
        return inner

    return wrapper


def clean_headers(raw_headers: str):
    is_name = True
    name: str = ''
    headers = {}
    for i, line in enumerate(filter(None, raw_headers.splitlines())):
        if not is_name:
            headers[name] = line
            is_name = True
            continue

        if line[-1] != ':':
            raise ValueError(f'Unexpected string: {line} on {i + 1}th line.')

        name = line[:-1]
        is_name = False

    return headers


class FullDunder:
    """
    Thanks to [this post](https://www.reddit.com/r/Python/comments/br9ok2/list_of_all_python_dunder_methods/),
    for making a full list of Python dunder methods.
    """
    def _callable_dunder_getattr(self, __name, *args, **kwargs):
        return __name, args, kwargs

    async def _callable_dunder_getattr_async(self, __name, *args, **kwargs):
        return __name, args, kwargs

    # @classmethod
    # def _callable_dunder_getattr_cls(cls, __name, *args, **kwargs):
    #     return getattr(cls, __name)(*args, **kwargs)

    # def __getattribute__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__getattribute__", *args, **kwargs)

    # def __getattr__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__getattr__", *args, **kwargs)

    # def __init__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__init__", *args, **kwargs)

    # @classmethod
    # def __init_subclass__(cls, *args, **kwargs):
    #     return cls._callable_dunder_getattr_cls("__init_subclass__", *args, **kwargs)

    # @classmethod
    # def __new__(cls, *args, **kwargs):
    #     return cls._callable_dunder_getattr_cls("__new__", *args, **kwargs)

    # @classmethod
    # def __class_getitem__(cls, *args, **kwargs):
    #     return cls._callable_dunder_getattr_cls("__class_getitem__", *args, **kwargs)

    def __delattr__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__delattr__", *args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__delitem__", *args, **kwargs)

    # def __delslice__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__delslice__", *args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__setattr__", *args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__setitem__", *args, **kwargs)

    # def __setslice__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__setslice__", *args, **kwargs)

    def __missing__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__missing__", *args, **kwargs)

    def __getitem__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__getitem__", *args, **kwargs)

    # def __getslice__(self, *args, **kwargs):
    #     return self._callable_dunder_getattr("__getslice__", *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__eq__", *args, **kwargs)

    def __ge__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ge__", *args, **kwargs)

    def __gt__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__gt__", *args, **kwargs)

    def __le__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__le__", *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ne__", *args, **kwargs)

    def __lt__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__lt__", *args, **kwargs)

    def __hash__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__hash__", *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__add__", *args, **kwargs)

    def __and__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__and__", *args, **kwargs)

    def __divmod__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__divmod__", *args, **kwargs)

    def __floordiv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__floordiv__", *args, **kwargs)

    def __lshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__lshift__", *args, **kwargs)

    def __matmul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__matmul__", *args, **kwargs)

    def __mod__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__mod__", *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__mul__", *args, **kwargs)

    def __or__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__or__", *args, **kwargs)

    def __pow__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__pow__", *args, **kwargs)

    def __rshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rshift__", *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__sub__", *args, **kwargs)

    def __truediv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__truediv__", *args, **kwargs)

    def __xor__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__xor__", *args, **kwargs)

    def __radd__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__radd__", *args, **kwargs)

    def __rand__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rand__", *args, **kwargs)

    def __rdiv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rdiv__", *args, **kwargs)

    def __rdivmod__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rdivmod__", *args, **kwargs)

    def __rfloordiv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rfloordiv__", *args, **kwargs)

    def __rlshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rlshift__", *args, **kwargs)

    def __rmatmul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rmatmul__", *args, **kwargs)

    def __rmod__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rmod__", *args, **kwargs)

    def __rmul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rmul__", *args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ror__", *args, **kwargs)

    def __rpow__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rpow__", *args, **kwargs)

    def __rrshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rrshift__", *args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rsub__", *args, **kwargs)

    def __rtruediv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rtruediv__", *args, **kwargs)

    def __rxor__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__rxor__", *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__iadd__", *args, **kwargs)

    def __iand__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__iand__", *args, **kwargs)

    def __ifloordiv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ifloordiv__", *args, **kwargs)

    def __ilshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ilshift__", *args, **kwargs)

    def __imatmul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__imatmul__", *args, **kwargs)

    def __imod__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__imod__", *args, **kwargs)

    def __imul__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__imul__", *args, **kwargs)

    def __ior__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ior__", *args, **kwargs)

    def __ipow__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ipow__", *args, **kwargs)

    def __irshift__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__irshift__", *args, **kwargs)

    def __isub__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__isub__", *args, **kwargs)

    def __itruediv__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__itruediv__", *args, **kwargs)

    def __ixor__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ixor__", *args, **kwargs)

    def __abs__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__abs__", *args, **kwargs)

    def __neg__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__neg__", *args, **kwargs)

    def __pos__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__pos__", *args, **kwargs)

    def __invert__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__invert__", *args, **kwargs)

    def __index__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__index__", *args, **kwargs)

    def __trunc__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__trunc__", *args, **kwargs)

    def __floor__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__floor__", *args, **kwargs)

    def __ceil__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__ceil__", *args, **kwargs)

    def __round__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__round__", *args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__iter__", *args, **kwargs)

    def __len__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__len__", *args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__reversed__", *args, **kwargs)

    def __contains__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__contains__", *args, **kwargs)

    def __next__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__next__", *args, **kwargs)

    def __int__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__int__", *args, **kwargs)

    def __bool__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__bool__", *args, **kwargs)

    def __nonzero__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__nonzero__", *args, **kwargs)

    def __complex__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__complex__", *args, **kwargs)

    def __float__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__float__", *args, **kwargs)

    def __format__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__format__", *args, **kwargs)

    def __cmp__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__cmp__", *args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__enter__", *args, **kwargs)

    def __exit__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__exit__", *args, **kwargs)

    def __get__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__get__", *args, **kwargs)

    def __set__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__set__", *args, **kwargs)

    def __delete__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__delete__", *args, **kwargs)

    def __set_name__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__set_name__", *args, **kwargs)

    async def __aenter__(self, *args, **kwargs):
        return await self._callable_dunder_getattr_async("__aenter__", *args, **kwargs)

    async def __aexit__(self, *args, **kwargs):
        return await self._callable_dunder_getattr_async("__aexit__", *args, **kwargs)

    async def __aiter__(self, *args, **kwargs):
        return await self._callable_dunder_getattr_async("__aiter__", *args, **kwargs)

    async def __anext__(self, *args, **kwargs):
        return await self._callable_dunder_getattr_async("__anext__", *args, **kwargs)

    async def __await__(self, *args, **kwargs):
        return await self._callable_dunder_getattr_async("__await__", *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__call__", *args, **kwargs)

    def __class__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__class__", *args, **kwargs)

    def __dir__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__dir__", *args, **kwargs)

    def __prepare__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__prepare__", *args, **kwargs)

    def __subclasses__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__subclasses__", *args, **kwargs)

    def __instancecheck__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__instancecheck__", *args, **kwargs)

    def __subclasscheck__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__subclasscheck__", *args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__str__", *args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__repr__", *args, **kwargs)

    def __import__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__import__", *args, **kwargs)

    def __bytes__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__bytes__", *args, **kwargs)

    def __fspath__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__fspath__", *args, **kwargs)

    def __getnewargs__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__getnewargs__", *args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__reduce__", *args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__reduce_ex__", *args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__sizeof__", *args, **kwargs)

    def __length_hint__(self, *args, **kwargs):
        return self._callable_dunder_getattr("__length_hint__", *args, **kwargs)
