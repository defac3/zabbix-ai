from pydantic import BaseModel


class LogLinesRequest(BaseModel):
    lines: list[str]

class AnalyseResponse(BaseModel):
    req: str
    reason: str


class FixResponse(BaseModel):
    cmd: str
    req: str
    reason: str
