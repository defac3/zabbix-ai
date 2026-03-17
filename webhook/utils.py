from __future__ import annotations

from typing import Any

from aiohttp import ClientSession

from const import API_URL, CA_PATH


async def call_api(
    session: ClientSession, path: str, body: dict[str, Any]
) -> dict[str, Any] | None:
    url = f"{API_URL}{path}"
    ssl: bool | Any = False
    if CA_PATH:
        import ssl as ssl_mod
        ssl = ssl_mod.create_default_context(cafile=CA_PATH)
    try:
        async with session.post(url, json=body, ssl=ssl) as resp:
            if resp.status != 200:
                return None
            return await resp.json()
    except Exception:
        return None
