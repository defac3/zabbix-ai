from pydantic import BaseModel


class LogLinesRequest(BaseModel):
    lines: list[str]


class AnalysisResponse(BaseModel):
    analysis: str


class SolutionResponse(BaseModel):
    solution: str
