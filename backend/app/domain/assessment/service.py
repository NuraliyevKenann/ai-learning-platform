"""Attempt submission and evaluation orchestration."""

import json

from app.domain.assessment.schemas import AttemptResultResponse
from app.domain.assessment.repository import record_attempt
from app.domain.content.repository import get_exercise_by_id
from app.domain.learning.repository import get_mastery, set_mastery
from app.domain.recommendations.service import (
    build_recommendation,
    save_current_recommendation,
)
from app.learning_engine.mastery import update_mastery


class ExerciseNotFoundError(Exception):
    """Raised when an attempt references an unknown exercise."""


def submit_attempt(
    user_id: str,
    exercise_id: str,
    answer: str,
) -> AttemptResultResponse:
    exercise = get_exercise_by_id(exercise_id)
    if exercise is None:
        raise ExerciseNotFoundError

    is_correct = _answers_match(
        submitted_answer=answer,
        expected_answer=str(exercise["expected_answer"]),
    )
    score = 100.0 if is_correct else 0.0

    skill_id = str(exercise["skill_id"])
    old_mastery = get_mastery(user_id, skill_id)
    new_mastery = update_mastery(old_mastery=old_mastery, attempt_score=score)
    set_mastery(user_id=user_id, skill_id=skill_id, mastery=new_mastery)
    record_attempt(
        user_id=user_id,
        exercise_id=exercise_id,
        answer=answer,
        is_correct=is_correct,
        score=score,
        old_mastery=old_mastery,
        new_mastery=new_mastery,
    )

    recommendation = build_recommendation(
        user_id=user_id,
        exercise_id=exercise_id,
        skill_id=skill_id,
        is_correct=is_correct,
        mastery=new_mastery,
    )
    save_current_recommendation(user_id, recommendation)

    return AttemptResultResponse(
        status="ok",
        exercise_id=exercise_id,
        is_correct=is_correct,
        score=score,
        old_mastery=old_mastery,
        new_mastery=new_mastery,
        recommendation=recommendation,
    )


def _answers_match(submitted_answer: str, expected_answer: str) -> bool:
    submitted_json = _parse_json(submitted_answer)
    expected_json = _parse_json(expected_answer)
    if submitted_json is not None and expected_json is not None:
        return submitted_json == expected_json

    return _normalize_text(submitted_answer) == _normalize_text(expected_answer)


def _parse_json(value: str) -> object | None:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _normalize_text(value: str) -> str:
    return "".join(value.lower().split())
