"""Recommendation request/response schemas."""

from pydantic import BaseModel


class Recommendation(BaseModel):
    type: str
    exercise_id: str | None
    reason: str


class CurrentRecommendationResponse(BaseModel):
    recommendation: Recommendation
