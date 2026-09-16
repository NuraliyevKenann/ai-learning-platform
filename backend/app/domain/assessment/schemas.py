"""Assessment request/response schemas."""

from datetime import datetime

from pydantic import BaseModel

from app.domain.recommendations.schemas import Recommendation


class SubmitAttemptRequest(BaseModel):
    exercise_id: str
    answer: str


class AttemptResultResponse(BaseModel):
    status: str
    exercise_id: str
    is_correct: bool
    score: float
    old_mastery: float
    new_mastery: float
    recommendation: Recommendation


class AttemptHistoryItem(BaseModel):
    id: int
    exercise_id: str
    answer: str
    is_correct: bool
    score: float
    old_mastery: float
    new_mastery: float
    created_at: datetime


class AttemptHistoryResponse(BaseModel):
    items: list[AttemptHistoryItem]
