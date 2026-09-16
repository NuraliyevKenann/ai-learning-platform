from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user
from app.domain.assessment.schemas import (
    AttemptResultResponse,
    SubmitAttemptRequest,
)
from app.domain.assessment.service import (
    ExerciseNotFoundError,
    submit_attempt as submit_attempt_to_service,
)
from app.domain.users.models import User

router = APIRouter()


@router.post("", response_model=AttemptResultResponse)
def submit_attempt(
    payload: SubmitAttemptRequest,
    user: User = Depends(get_current_user),
) -> AttemptResultResponse:
    try:
        return submit_attempt_to_service(
            user_id=user.id,
            exercise_id=payload.exercise_id,
            answer=payload.answer,
        )
    except ExerciseNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found.",
        ) from exc
