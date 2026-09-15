from fastapi import APIRouter, HTTPException, status

from app.domain.assessment.schemas import (
    AttemptResultResponse,
    SubmitAttemptRequest,
)
from app.domain.assessment.service import (
    ExerciseNotFoundError,
    submit_attempt as submit_attempt_to_service,
)

router = APIRouter()


@router.post("", response_model=AttemptResultResponse)
def submit_attempt(payload: SubmitAttemptRequest) -> AttemptResultResponse:
    try:
        return submit_attempt_to_service(
            exercise_id=payload.exercise_id,
            answer=payload.answer,
        )
    except ExerciseNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found.",
        ) from exc
