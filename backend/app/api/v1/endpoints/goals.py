from fastapi import APIRouter

from app.domain.content.schemas import GoalListResponse
from app.domain.content.service import list_goals as list_goals_from_service

router = APIRouter()


@router.get("", response_model=GoalListResponse)
def list_goals() -> GoalListResponse:
    return GoalListResponse(items=list_goals_from_service())
