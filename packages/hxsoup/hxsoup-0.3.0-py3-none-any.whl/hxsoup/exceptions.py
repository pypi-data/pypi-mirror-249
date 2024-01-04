from __future__ import annotations

from httpx import codes


class EmptyResultError(Exception):
    def __init__(self, error_message: str, selector: str | None = None, url=None, status_code: int | None = None) -> None:
        error_message += (
            ' This error happens probably because of invalid selector or URL. '
            'Check whether selector and URL are both valid.\n'
        )

        if status_code is not None:
            error_message += f"status code: HTTP {status_code} {codes(200).name}, "

        if url is not None:
            error_message += f"URL: {url}, "

        error_message += f'selector: {selector!r}'

        super().__init__(error_message)
