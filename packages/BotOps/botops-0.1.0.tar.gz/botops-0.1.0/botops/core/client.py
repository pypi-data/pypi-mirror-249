from dataclasses import dataclass, field
from http.client import HTTPException
from typing import Any, Literal, Self

import aiohttp

__all__ = ["APIClient"]


@dataclass(frozen=True, slots=True, kw_only=True)
class _Response:
    ok: bool = field()
    result: list[dict] | dict | bool | None = field(default=None)
    error_code: str | None = field(default=None)
    description: str | None = field(default=None)


class APIClient:
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession("https://api.telegram.org")

    async def setup(self) -> Self:
        return self

    async def shutdown(self) -> None:
        await self.session.close()

    async def request(
        self, method: Literal["POST", "GET"], path: str, /, **attrs: Any
    ) -> _Response:
        for k, v in tuple(attrs.items()):
            if v is None:
                attrs.pop(k, None)

        if method == "GET":
            request = self.session.request(method, path, params=attrs)
        else:
            request = self.session.request(method, path, json=attrs)

        async with request as response:
            if response.status != 200:
                raise HTTPException(await response.text())

            raw_data = await response.json()

        return _Response(**raw_data)
