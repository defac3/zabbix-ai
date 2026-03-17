from __future__ import annotations

from const import API_URL

from typing import TYPE_CHECKING
if TYPE_CHECKING:

    from typing import Any, Dict, Union
    from aiohttp import ClientSession


async def call_api(
    session: "ClientSession", 
    path: str, 
    body: "Dict[str, Any]"
) -> "Union[Dict[str, Any], None]":

    url = f"{API_URL}{path}"
    async with session.post(url, json=body, ssl=False) as resp:
        if resp.status != 200:
            return None
        return await resp.json()
