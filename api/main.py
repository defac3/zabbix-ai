from contextlib import asynccontextmanager

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from fastapi import FastAPI, HTTPException

from models import (
    LogLinesRequest,
    AnalysisResponse,
    SolutionResponse,
)
from const import OLLAMA_URL, OLLAMA_MODEL

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, AsyncGenerator


class App:
    def init(self, ollama_url: str, ollama_model: str):
        self._client: "Optional[ClientSession]" = None

        self.ollama_url = ollama_url
        self.ollama_model = ollama_model

    @asynccontextmanager
    @staticmethod
    async def lifespan(app: "FastAPI") -> "AsyncGenerator[None, None]":
        yield

    @property
    def app(self) -> "FastAPI":
        if self._app is None:
            self._app = FastAPI(
                lifespan=self.lifespan,
                docs_url=None,
                redoc_url=None
            )
        return self._app

    @property
    def session(self) -> "ClientSession":
        if self._session is None:
            self._session = ClientSession(timeout=float(2))
        return self._session

    async def __call__(self) -> "FastAPI":
        return self.app


    @classmethod
    async def _check_ollama(cls) -> bool:
        try:
            async with cls.session as client:
                async with client.get(f"{OLLAMA_URL}/api/tags") as response:
                    return response.status == 200
        except:
            return False

    async def _generate(self, prompt: str) -> str:
        async with self.session as client:
            try:
                r = await client.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": OLLAMA_MODEL, 
                        "prompt": prompt, 
                        "stream": False
                    },
                )
                r.raise_for_status()
                data = r.json()
                return data.get("response", "").strip()
            except ClientResponseError as e:
                raise HTTPException(
                    status_code=502,
                    detail=f"Error: {e}",
                )

    @app.get("/health")
    async def health(self):
        ollama_ok = await self._check_ollama()
        return {"status": "ok", "ollama": ollama_ok}


    @app.post("/analyse", response_model=AnalysisResponse)
    async def analyse(self, body: LogLinesRequest):
        if not body.lines:
            raise HTTPException(status_code=400, detail="Lines must not be empty")
        prompt = (
            "Analyze these log lines. Describe what is wrong or what they indicate. "
            "Reply only with the analysis, no preamble.\n\nLog lines:\n"
            + "\n".join(body.lines)
        )
        text = await self._generate(prompt)
        return AnalysisResponse(analysis=text or str())


    @app.post("/fix", response_model=SolutionResponse)
    async def fix(self, body: LogLinesRequest):
        if not body.lines:
            raise HTTPException(status_code=400, detail="lines must not be empty")
        prompt = (
            "These are problematic log lines. Suggest a concrete fix or solution. "
            "Reply only with the solution steps, no preamble.\n\nLog lines:\n"
            + "\n".join(body.lines)
        )
        text = await self._generate(prompt)
        return SolutionResponse(solution=text or str())

if __name__ == "app":
    app = App(OLLAMA_URL, OLLAMA_MODEL)
