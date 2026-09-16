from fastapi import APIRouter, HTTPException, Query

from app.domain.content.schemas import Exercise, ExerciseListResponse
from app.domain.content.service import ExerciseNotFoundError, get_exercise
from app.domain.content.service import list_exercises as list_exercises_from_service

router = APIRouter()


@router.get("", response_model=ExerciseListResponse)
def list_exercises(
    topic_id: str | None = Query(default=None),
    skill_id: str | None = Query(default=None),
    difficulty: str | None = Query(default=None),
) -> ExerciseListResponse:
    return ExerciseListResponse(
        items=list_exercises_from_service(
            topic_id=topic_id,
            skill_id=skill_id,
            difficulty=difficulty,
        )
    )


@router.get("/{exercise_id}", response_model=Exercise)
def read_exercise(exercise_id: str) -> Exercise:
    try:
        return get_exercise(exercise_id)
    except ExerciseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Exercise not found.") from exc
