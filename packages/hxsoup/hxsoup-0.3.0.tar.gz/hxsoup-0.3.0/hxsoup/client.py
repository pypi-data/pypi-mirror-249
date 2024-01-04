from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
import logging
import typing
from frozendict import frozendict

from httpx import (
    AsyncClient as _HttpxAsyncClient,
    Client as _HttpxClient,
    RequestError,
    HTTPStatusError,
    Response,
)
from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault, EventHook
from httpx._config import (
    DEFAULT_LIMITS,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT_CONFIG,
    Limits,
)
from httpx._transports.base import AsyncBaseTransport, BaseTransport
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from .souptools import Parsers, SoupedResponse, _resolve_default

DEV_HEADERS = frozendict({
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Arch": '"x86"',
    "Sec-Ch-Ua-Bitness": '"64"',
    "Sec-Ch-Ua-Full-Version-List": '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.130", "Google Chrome";v="120.0.6099.130"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Model": '""',
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
})
DEV_DEFAULT_TIMEOUT_CONFIG = 5.0


class Client(_HttpxClient):
    def __init__(
        self,
        *,
        auth: typing.Optional[AuthTypes] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        verify: VerifyTypes = True,
        cert: typing.Optional[CertTypes] = None,
        http1: bool = True,
        http2: bool = False,
        proxy: typing.Optional[ProxyTypes] = None,
        proxies: typing.Optional[ProxiesTypes] = None,
        mounts: typing.Optional[
            typing.Mapping[str, typing.Optional[BaseTransport]]
        ] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Optional[
            typing.Mapping[str, typing.List[EventHook]]
        ] = None,
        base_url: URLTypes = "",
        transport: typing.Optional[BaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool = True,
        default_encoding: typing.Union[str, typing.Callable[[bytes], str]] = "utf-8",
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        self.attempts = attempts
        self.raise_for_status = raise_for_status
        self.parser: Parsers | None = parser
        self.broadcasting = broadcasting
        self.no_empty_result = no_empty_result

        return super().__init__(
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
        )

    def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> SoupedResponse:
        attempts = _resolve_default(attempts, self.attempts, 1)
        raise_for_status = _resolve_default(raise_for_status, self.raise_for_status, False)
        parser = _resolve_default(parser, self.parser, allow_none=True)
        broadcasting = _resolve_default(broadcasting, self.broadcasting, allow_none=True)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, allow_none=True)

        for i in range(attempts):
            try:
                response = super().request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
            except (RequestError, HTTPStatusError):
                if i == attempts - 1:
                    raise
                logging.warning("Retrying...")
            else:
                if i > 0:
                    logging.warning(f"Successfully retrieved: '{url}'")
                if raise_for_status:
                    response.raise_for_status()
                return SoupedResponse(
                    response,
                    parser=parser,
                    broadcasting=broadcasting,
                    no_empty_result=no_empty_result,
                )
        raise  # Unreachable

    @contextmanager
    def stream(
        self,
        method: str,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> typing.Iterator[SoupedResponse]:
        attempts = _resolve_default(attempts, self.attempts, 1)
        raise_for_status = _resolve_default(raise_for_status, self.raise_for_status, False)
        parser = _resolve_default(parser, self.parser, allow_none=True)
        broadcasting = _resolve_default(broadcasting, self.broadcasting, allow_none=True)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, allow_none=True)

        for i in range(attempts):
            try:
                request = self.build_request(
                    method=method,
                    url=url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    extensions=extensions,
                )
                response = self.send(
                    request=request,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    stream=True,
                )
            except (RequestError, HTTPStatusError):
                if i == attempts - 1:
                    raise
                logging.warning("Retrying...")
            else:
                if i > 0:
                    logging.warning(f"Successfully retrieved: '{url}'")
                if raise_for_status:
                    response.raise_for_status()
                try:
                    yield SoupedResponse(
                        response,
                        parser=parser,
                        broadcasting=broadcasting,
                        no_empty_result=no_empty_result,
                    )
                finally:
                    response.close()
                    return
        raise  # Unreachable

    def get(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `GET` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def options(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send an `OPTIONS` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def head(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `HEAD` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "HEAD",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def post(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `POST` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def put(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `PUT` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def patch(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `PATCH` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def delete(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `DELETE` request.

        **Parameters**: See `httpx.request`.
        """
        return self.request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )


class AsyncClient(_HttpxAsyncClient):
    def __init__(
        self,
        *,
        auth: typing.Optional[AuthTypes] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        verify: VerifyTypes = True,
        cert: typing.Optional[CertTypes] = None,
        http1: bool = True,
        http2: bool = False,
        proxy: typing.Optional[ProxyTypes] = None,
        proxies: typing.Optional[ProxiesTypes] = None,
        mounts: typing.Optional[
            typing.Mapping[str, typing.Optional[AsyncBaseTransport]]
        ] = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Optional[
            typing.Mapping[str, typing.List[typing.Callable[..., typing.Any]]]
        ] = None,
        base_url: URLTypes = "",
        transport: typing.Optional[AsyncBaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool = True,
        default_encoding: typing.Union[str, typing.Callable[[bytes], str]] = "utf-8",
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        self.attempts = attempts
        self.raise_for_status = raise_for_status
        self.parser: Parsers | None = parser
        self.broadcasting = broadcasting
        self.no_empty_result = no_empty_result

        super().__init__(
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
        )

    async def request(
        self,
        method: str,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> SoupedResponse:
        attempts = _resolve_default(attempts, self.attempts, 1)
        raise_for_status = _resolve_default(raise_for_status, self.raise_for_status, False)
        parser = _resolve_default(parser, self.parser, allow_none=True)
        broadcasting = _resolve_default(broadcasting, self.broadcasting, allow_none=True)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, allow_none=True)

        for i in range(attempts):
            try:
                response = await super().request(
                    method,
                    url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    timeout=timeout,
                    extensions=extensions,
                )
            except (RequestError, HTTPStatusError):
                if i == attempts - 1:
                    raise
                logging.warning("Retrying...")
            else:
                if i > 0:
                    logging.warning(f"Successfully retrieved: '{url}'")
                if raise_for_status:
                    response.raise_for_status()
                return SoupedResponse(
                    response,
                    parser=parser,
                    broadcasting=broadcasting,
                    no_empty_result=no_empty_result,
                )
        raise  # Unreachable

    @asynccontextmanager
    async def stream(
        self,
        method: str,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> typing.AsyncIterator[SoupedResponse]:
        """
        Alternative to `httpx.request()` that streams the response body
        instead of loading it into memory at once.

        **Parameters**: See `httpx.request`.

        See also: [Streaming Responses][0]

        [0]: /quickstart#streaming-responses
        """
        attempts = _resolve_default(attempts, self.attempts, 1)
        raise_for_status = _resolve_default(raise_for_status, self.raise_for_status, False)
        parser = _resolve_default(parser, self.parser, allow_none=True)
        broadcasting = _resolve_default(broadcasting, self.broadcasting, allow_none=True)
        no_empty_result = _resolve_default(no_empty_result, self.no_empty_result, allow_none=True)

        for i in range(attempts):
            try:
                request = self.build_request(
                    method=method,
                    url=url,
                    content=content,
                    data=data,
                    files=files,
                    json=json,
                    params=params,
                    headers=headers,
                    cookies=cookies,
                    timeout=timeout,
                    extensions=extensions,
                )
                response = await self.send(
                    request=request,
                    auth=auth,
                    follow_redirects=follow_redirects,
                    stream=True,
                )
            except (RequestError, HTTPStatusError):
                if i == attempts - 1:
                    raise
                logging.warning("Retrying...")
            else:
                if i > 0:
                    logging.warning(f"Successfully retrieved: '{url}'")
                if raise_for_status:
                    response.raise_for_status()
                try:
                    yield SoupedResponse(
                        response,
                        parser=parser,
                        broadcasting=broadcasting,
                        no_empty_result=no_empty_result,
                    )
                finally:
                    await response.aclose()
                    return
        raise  # Unreachable

    async def get(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault, None] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `GET` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "GET",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def options(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send an `OPTIONS` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "OPTIONS",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def head(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `HEAD` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "HEAD",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def post(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `POST` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "POST",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def put(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `PUT` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "PUT",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def patch(
        self,
        url: URLTypes,
        *,
        content: typing.Optional[RequestContent] = None,
        data: typing.Optional[RequestData] = None,
        files: typing.Optional[RequestFiles] = None,
        json: typing.Optional[typing.Any] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `PATCH` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "PATCH",
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    async def delete(
        self,
        url: URLTypes,
        *,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = None,
        cookies: typing.Optional[CookieTypes] = None,
        auth: typing.Union[AuthTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        follow_redirects: typing.Union[bool, UseClientDefault] = USE_CLIENT_DEFAULT,
        timeout: typing.Union[TimeoutTypes, UseClientDefault] = USE_CLIENT_DEFAULT,
        extensions: typing.Optional[RequestExtensions] = None,
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> Response:
        """
        Send a `DELETE` request.

        **Parameters**: See `httpx.request`.
        """
        return await self.request(
            "DELETE",
            url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )


class DevClient(Client):
    def __init__(
        self,
        *,
        auth: typing.Optional[AuthTypes] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = DEV_HEADERS,  # changed
        cookies: typing.Optional[CookieTypes] = None,
        verify: VerifyTypes = True,
        cert: typing.Optional[CertTypes] = None,
        http1: bool = True,
        http2: bool = False,
        proxy: typing.Optional[ProxyTypes] = None,
        proxies: typing.Optional[ProxiesTypes] = None,
        mounts: typing.Optional[
            typing.Mapping[str, typing.Optional[BaseTransport]]
        ] = None,
        timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,  # changed
        follow_redirects: bool = True,  # changed
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Optional[
            typing.Mapping[str, typing.List[EventHook]]
        ] = None,
        base_url: URLTypes = "",
        transport: typing.Optional[BaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool = True,
        default_encoding: typing.Union[str, typing.Callable[[bytes], str]] = "utf-8",
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = True,  # changed
        no_empty_result: bool | None = None,
    ) -> None:
        return super().__init__(
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


class DevAsyncClient(AsyncClient):
    def __init__(
        self,
        *,
        auth: typing.Optional[AuthTypes] = None,
        params: typing.Optional[QueryParamTypes] = None,
        headers: typing.Optional[HeaderTypes] = DEV_HEADERS,  # changed
        cookies: typing.Optional[CookieTypes] = None,
        verify: VerifyTypes = True,
        cert: typing.Optional[CertTypes] = None,
        http1: bool = True,
        http2: bool = False,
        proxy: typing.Optional[ProxyTypes] = None,
        proxies: typing.Optional[ProxiesTypes] = None,
        mounts: typing.Optional[
            typing.Mapping[str, typing.Optional[AsyncBaseTransport]]
        ] = None,
        timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,  # changed
        follow_redirects: bool = True,  # changed
        limits: Limits = DEFAULT_LIMITS,
        max_redirects: int = DEFAULT_MAX_REDIRECTS,
        event_hooks: typing.Optional[
            typing.Mapping[str, typing.List[typing.Callable[..., typing.Any]]]
        ] = None,
        base_url: URLTypes = "",
        transport: typing.Optional[AsyncBaseTransport] = None,
        app: typing.Optional[typing.Callable[..., typing.Any]] = None,
        trust_env: bool = True,
        default_encoding: typing.Union[str, typing.Callable[[bytes], str]] = "utf-8",
        attempts: int | None = None,
        raise_for_status: bool | None = None,
        parser: Parsers | None = None,
        broadcasting: bool | None = True,  # changed
        no_empty_result: bool | None = None,
    ) -> None:
        super().__init__(
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
