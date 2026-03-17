from __future__ import annotations

from aiohttp import ClientSession


class ZabbixAPI:
    def __init__(
        self,
        url: str,
        user: str,
        password: str,
        script_id: str,
    ) -> None:
        self._url = url.rstrip("/")
        self._user = user
        self._password = password
        self._script_id = script_id

    async def login(self, session: ClientSession) -> str | None:
        payload = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {"username": self._user, "password": self._password},
            "id": 1,
        }
        try:
            async with session.post(f"{self._url}/api_jsonrpc.php", json=payload) as resp:
                if resp.status != 200:
                    return None
                data = await resp.json()
                return data.get("result")
        except Exception:
            return None

    async def execute(
        self,
        session: ClientSession,
        hostid: str,
        cmd: str,
        *,
        auth: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> bool:
        if not self._script_id or not hostid:
            return False
        payload = {
            "jsonrpc": "2.0",
            "method": "script.execute",
            "params": {
                "scriptid": self._script_id,
                "hostid": hostid,
                "params": [cmd],
            },
            "id": 2,
        }
        if auth is not None:
            payload["auth"] = auth
        try:
            async with session.post(
                f"{self._url}/api_jsonrpc.php", json=payload, headers=headers or {}
            ) as resp:
                return resp.status == 200
        except Exception:
            return False
