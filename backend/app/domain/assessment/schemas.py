"""Assessment request/response schemas."""

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
