from json import loads, JSONDecodeError
from re import search, sub

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientResponseError

from const import OLLAMA_URL, OLLAMA_MODEL, LLM_MAX_RETRIES

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Tuple


class OllamaClient:
    def __init__(
        self,
        url: str = OLLAMA_URL,
        model: str = OLLAMA_MODEL,
        max_retries: int = LLM_MAX_RETRIES,
    ):
        self.url = url
        self.model = model
        self.max_retries = max_retries
        self._session: "Optional[ClientSession]" = None

    @property
    def session(self) -> ClientSession:
        if self._session is None or self._session.closed:
            self._session = ClientSession(timeout=ClientTimeout(total=120))
        return self._session

    async def check(self) -> bool:
        try:
            async with self.session.get(f"{self.url}/api/tags") as r:
                return r.status == 200
        except Exception:
            return False

    async def generate(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
        }
        async with self.session.post(f"{self.url}/api/chat", json=payload) as r:
            r.raise_for_status()
            data = await r.json()
            return (data.get("message", {}).get("content", "")).strip()

    async def generate_json(
        self,
        system: str,
        user: str,
        required_keys: "Tuple[str, ...]",
    ) -> dict:
        last_text = ""
        for _ in range(1, self.max_retries + 1):
            try:
                text = await self.generate(system, user)
                last_text = text
                data = self.extract_json(text)
                if data is None:
                    continue
                missing = [k for k in required_keys if k not in data]
                if missing:
                    continue
                return {k: str(data[k]) for k in required_keys}
            except ClientResponseError:
                raise
            except Exception:
                continue
        raise ValueError(
            f"Model did not return valid JSON after {self.max_retries} attempts. "
            f"Last output: {last_text[:300]}"
        )

    @staticmethod
    def extract_json(text: str) -> "Optional[dict]":
        text = (text or "").strip()
        if "```" in text:
            m = search(r"```(?:json)?\s*([\s\S]*?)```", text)
            if m:
                text = m.group(1).strip()
        text = sub(r",\s*}", "}", text)
        try:
            data = loads(text)
            if isinstance(data, dict):
                return data
        except (JSONDecodeError, TypeError):
            pass
        start = text.find("{")
        if start == -1:
            return None
        depth = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        raw = sub(r",\s*}", "}", text[start : i + 1])
                        data = loads(raw)
                        return data if isinstance(data, dict) else None
                    except (JSONDecodeError, TypeError):
                        pass
                    break
