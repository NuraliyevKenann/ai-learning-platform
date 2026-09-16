"""Attempt submission and evaluation orchestration."""

import json

from app.domain.assessment.repository import list_attempt_history, record_attempt
from app.domain.assessment.schemas import AttemptHistoryResponse, AttemptResultResponse
from app.domain.content.repository import get_exercise_by_id
from app.domain.learning.repository import get_mastery, set_mastery
from app.domain.recommendations.service import (
    build_recommendation,
    save_current_recommendation,
)
from app.learning_engine.mastery import update_mastery


class ExerciseNotFoundError(Exception):
    """Raised when an attempt references an unknown exercise."""


def get_attempt_history(user_id: str) -> AttemptHistoryResponse:
    return AttemptHistoryResponse(items=list_attempt_history(user_id))


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
        expected_answers=_expected_answers(exercise),
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
        feedback=_build_feedback(exercise=exercise, is_correct=is_correct),
        hint=None if is_correct else str(exercise["hint"]),
        solution=str(exercise["solution"]),
        explanation=str(exercise["explanation"]),
        recommendation=recommendation,
    )


def _expected_answers(exercise: dict) -> list[str]:
    answers = [str(exercise["expected_answer"])]
    answers.extend(str(answer) for answer in exercise.get("acceptable_answers", []))
    return answers


def _build_feedback(exercise: dict, is_correct: bool) -> str:
    if is_correct:
        return "Correct. Review the explanation, then continue with the recommendation."
    return str(exercise["incorrect_feedback"])


def _answers_match(submitted_answer: str, expected_answers: list[str]) -> bool:
    return any(
        _single_answer_matches(submitted_answer=submitted_answer, expected_answer=expected_answer)
        for expected_answer in expected_answers
    )


def _single_answer_matches(submitted_answer: str, expected_answer: str) -> bool:
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
