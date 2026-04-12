from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Unstructured text to analyze")


class AnalyzeResponse(BaseModel):
    summary: str
    action_items: list[str]
    next_step: str
    raw_output: str | None = None
