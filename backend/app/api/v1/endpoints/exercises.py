from fastapi import APIRouter

from app.domain.content.schemas import ExerciseListResponse
from app.domain.content.service import list_exercises as list_exercises_from_service

router = APIRouter()


@router.get("", response_model=ExerciseListResponse)
def list_exercises() -> ExerciseListResponse:
    return ExerciseListResponse(items=list_exercises_from_service())
