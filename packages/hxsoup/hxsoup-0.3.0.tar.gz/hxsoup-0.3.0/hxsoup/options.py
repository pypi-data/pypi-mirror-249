from __future__ import annotations

import typing

from httpx._client import EventHook
from httpx._config import Limits
from httpx._transports.base import BaseTransport
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from .souptools import Parsers
from .client import Client, DevClient, AsyncClient, DevAsyncClient
from .api import request
from .souptools import SoupedResponse


ALLOWED_KEYWORDS = frozenset({
    "auth",
    "params",
    "headers",
    "cookies",
    "verify",
    "cert",
    "http1",
    "http2",
    "proxy",
    "proxies",
    "mounts",
    "timeout",
    "follow_redirects",
    "limits",
    "max_redirects",
    "event_hooks",
    "base_url",
    "transport",
    "app",
    "trust_env",
    "default_encoding",
    "attempts",
    "raise_for_status",
    "parser",
    "broadcasting",
    "no_empty_result",
})
ALLOWED_KEYWORDS_IN_API = frozenset({
    "params",
    "headers",
    "cookies",
    "auth",
    "proxy",
    "proxies",
    "follow_redirects",
    "cert",
    "verify",
    "timeout",
    "trust_env",
    "attempts",
    "raise_for_status",
})


class ClientOptions:
    __slots__ = ("_kwargs",)
    auth: typing.Optional[AuthTypes]
    params: typing.Optional[QueryParamTypes]
    headers: typing.Optional[HeaderTypes]
    cookies: typing.Optional[CookieTypes]
    verify: VerifyTypes | None
    cert: typing.Optional[CertTypes]
    http1: bool | None
    http2: bool | None
    proxy: typing.Optional[ProxyTypes]
    proxies: typing.Optional[ProxiesTypes]
    mounts: typing.Optional[
        typing.Mapping[str, typing.Optional[BaseTransport]]
    ]
    timeout: TimeoutTypes
    follow_redirects: bool | None
    limits: Limits | None
    max_redirects: int | None
    event_hooks: typing.Optional[
        typing.Mapping[str, typing.List[EventHook]]
    ]
    base_url: URLTypes | None
    transport: typing.Optional[BaseTransport]
    app: typing.Optional[typing.Callable[..., typing.Any]]
    trust_env: bool | None
    default_encoding: typing.Union[str, typing.Callable[[bytes], str]] | None
    attempts: int | None
    raise_for_status: bool | None
    parser: Parsers | None
    broadcasting: bool | None
    no_empty_result: bool | None

    def __init__(
        self,
        *,
        auth: typing.Optional[AuthTypes] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        verify: VerifyTypes | None = None,
        cert: typing.Optional[CertTypes] = None,
        http1: bool | None = None,
        http2: bool | None = None,
        proxy: typing.Optional[ProxyTypes] = None,
        proxies: typing.Optional[ProxiesTypes] = None,
        mounts: typing.Optional[
            typing.Mapping[str, typing.Optional[BaseTransport]]
        ] = None,
        timeout: TimeoutTypes = None,
        follow_redirects: bool | None = None,
        limits: Limits | None = None,
        max_redirects: int | None = None,
        event_hooks: typing.Optional[
            typing.Mapping[str, typing.List[EventHook]]
        ] = None,
        base_url: URLTypes | None = None,
        transport: typing.Optional[BaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool | None = None,
        default_encoding: typing.Union[str, typing.Callable[[bytes], str]] | None = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        kwargs = dict(
            auth=auth,
            params=params,
            headers=headers,
            cookies=cookies,
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            proxy=proxy,
            proxies=proxies,
            mounts=mounts,
            timeout=timeout,
            follow_redirects=follow_redirects,
            limits=limits,
            max_redirects=max_redirects,
            event_hooks=event_hooks,
            base_url=base_url,
            transport=transport,
            app=app,
            trust_env=trust_env,
            default_encoding=default_encoding,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if value is not None
        }
        if hasattr(self, "_kwargs"):
            self._kwargs.update(kwargs)
        else:
            self._kwargs: dict = kwargs

    update = __init__

    def __repr__(self) -> str:
        options_str = ", ".join(f"{key}={value}" for key, value in self._kwargs.items())
        return f"{self.__class__.__qualname__}({options_str})"

    def build_client(self) -> Client:
        return Client(**self._kwargs)

    def build_async_client(self) -> AsyncClient:
        return AsyncClient(**self._kwargs)

    def _build_api_kwargs(self, copy: bool = False) -> dict:
        if not copy and ALLOWED_KEYWORDS_IN_API.issuperset(self._kwargs):
            return self._kwargs

        return {
            key: value
            for key, value in self._kwargs.items()
            if ALLOWED_KEYWORDS_IN_API
        }

    def request(self, *args, **kwargs) -> SoupedResponse:
        kwargs_to_use = self._build_api_kwargs(copy=True)
        kwargs_to_use.update(kwargs)

        return request(*args, **kwargs_to_use)

    def get(self, *args, **kwargs) -> SoupedResponse:
        return self.request("GET", *args, **kwargs)

    def options(self, *args, **kwargs) -> SoupedResponse:
        return self.request("OPTIONS", *args, **kwargs)

    def head(self, *args, **kwargs) -> SoupedResponse:
        return self.request("HEAD", *args, **kwargs)

    def post(self, *args, **kwargs) -> SoupedResponse:
        return self.request("POST", *args, **kwargs)

    def put(self, *args, **kwargs) -> SoupedResponse:
        return self.request("PUT", *args, **kwargs)

    def patch(self, *args, **kwargs) -> SoupedResponse:
        return self.request("PATCH", *args, **kwargs)

    def delete(self, *args, **kwargs) -> SoupedResponse:
        return self.request("DELETE", *args, **kwargs)

    def __getattr__(self, __name: str):
        if __name in ALLOWED_KEYWORDS:
            return self._kwargs[__name]
        raise AttributeError(f"'{self.__class__.__qualname__}' object has no attribute '{__name}'")


class MutableClientOptions(ClientOptions):
    def __eq__(self, other: MutableClientOptions) -> bool:
        return self._kwargs == other._kwargs

    def __setattr__(self, __name: str, __value) -> None:
        if __name == "_kwargs":
            super().__setattr__(__name, __value)
        elif __name in ALLOWED_KEYWORDS:
            self.update(**{__name: __value})
        else:
            raise AttributeError(f"'{self.__class__.__qualname__}' object has no attribute '{__name}'")


class DevClientOptions(ClientOptions):
    def build_client(self) -> DevClient:
        return DevClient(**self._kwargs)

    def build_async_client(self) -> DevAsyncClient:
        return DevAsyncClient(**self._kwargs)


class DevMutableClientOptions(DevClientOptions, MutableClientOptions):
    pass
