from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.recommendations.schemas import CurrentRecommendationResponse
from app.domain.recommendations.service import (
    get_current_recommendation as get_current_recommendation_from_service,
)
from app.domain.users.models import User

router = APIRouter()


@router.get("/current", response_model=CurrentRecommendationResponse)
def get_current_recommendation(
    user: User = Depends(get_current_user),
) -> CurrentRecommendationResponse:
    return CurrentRecommendationResponse(
        recommendation=get_current_recommendation_from_service(user.id)
    )
