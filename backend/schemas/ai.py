from pydantic import BaseModel


class AISummaryResponse(BaseModel):
    summary: str


class AISuggestRequest(BaseModel):
    title: str


class AISuggestResponse(BaseModel):
    description: str
    due_date: str


class AIInsightsResponse(BaseModel):
    summary: str
