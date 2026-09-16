"""Dashboard request/response schemas."""

from pydantic import BaseModel

from app.domain.assessment.schemas import AttemptHistoryItem
from app.domain.content.schemas import Exercise, Goal
from app.domain.learning.schemas import KnowledgeStateItem
from app.domain.recommendations.schemas import Recommendation
from app.domain.users.schemas import UserResponse


class DashboardSummaryResponse(BaseModel):
    user: UserResponse
    goal: Goal | None
    current_exercise: Exercise | None
    current_recommendation: Recommendation
    knowledge: list[KnowledgeStateItem]
    recent_attempts: list[AttemptHistoryItem]
    average_mastery: int
    completed_skills: int
    total_skills: int
    total_attempts: int
    correct_attempts: int
