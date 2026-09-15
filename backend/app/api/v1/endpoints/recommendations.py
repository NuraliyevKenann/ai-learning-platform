from fastapi import APIRouter

from app.domain.recommendations.schemas import CurrentRecommendationResponse
from app.domain.recommendations.service import (
    get_current_recommendation as get_current_recommendation_from_service,
)

router = APIRouter()


@router.get("/current", response_model=CurrentRecommendationResponse)
def get_current_recommendation() -> CurrentRecommendationResponse:
    return CurrentRecommendationResponse(
        recommendation=get_current_recommendation_from_service()
    )
