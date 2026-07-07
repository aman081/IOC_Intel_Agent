from typing import Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    ioc: str = Field(..., min_length=1, max_length=2048)


class SourceResult(BaseModel):
    source: str
    available: bool
    cached: bool = False
    data: dict[str, Any] = {}
    error: str | None = None


class AnalyzeResponse(BaseModel):
    ioc: str
    normalized_ioc: str
    type: str
    score: int
    verdict: str
    reasons: list[str]
    recommendation: str
    sources: dict[str, SourceResult]
