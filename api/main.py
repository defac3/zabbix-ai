from fastapi import FastAPI, HTTPException

from utils import OllamaClient
from prompts import (
    ANALYSE_SYSTEM, 
    ANALYSE_USER, 
    FIX_SYSTEM, 
    FIX_USER,
)
from models import LogLinesRequest, AnalyseResponse, FixResponse

client = OllamaClient()
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/health",)
async def health():
    ok = await client.check()
    return {"reason": "ok" if ok else "ollama unreachable"}

@app.post("/analyse", response_model=AnalyseResponse)
async def analyse(body: LogLinesRequest):
    if not body.lines:
        raise HTTPException(status_code=400, detail="lines must not be empty")
    req = "\n".join(body.lines)
    try:
        data = await client.generate_json(
            system=ANALYSE_SYSTEM,
            user=ANALYSE_USER.format(lines=req),
            required_keys=("reason",),
        )
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return AnalyseResponse(req=req, reason=data["reason"])


@app.post("/fix", response_model=FixResponse)
async def fix(body: LogLinesRequest):
    if not body.lines:
        raise HTTPException(status_code=400, detail="lines must not be empty")
    req = "\n".join(body.lines)
    try:
        data = await client.generate_json(
            system=FIX_SYSTEM,
            user=FIX_USER.format(lines=req),
            required_keys=("cmd", "reason"),
        )
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    return FixResponse(cmd=data["cmd"], req=req, reason=data["reason"])
