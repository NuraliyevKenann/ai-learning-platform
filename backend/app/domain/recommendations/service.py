"""Recommendation application service."""

from app.domain.assessment.repository import list_attempt_history
from app.domain.content.repository import list_exercises_with_answers
from app.domain.learning.repository import list_skill_mastery
from app.domain.recommendations.repository import (
    get_current_recommendation as get_current_recommendation_from_repository,
)
from app.domain.recommendations.repository import set_current_recommendation
from app.domain.recommendations.schemas import Recommendation
from app.learning_engine.rules import classify_mastery


def get_current_recommendation(user_id: str) -> Recommendation:
    return Recommendation(**get_current_recommendation_from_repository(user_id))


def save_current_recommendation(user_id: str, recommendation: Recommendation) -> None:
    set_current_recommendation(user_id, recommendation.model_dump())


def build_recommendation(
    user_id: str,
    exercise_id: str,
    skill_id: str,
    is_correct: bool,
    mastery: float,
) -> Recommendation:
    if not is_correct:
        return Recommendation(
            type="retry_exercise",
            exercise_id=exercise_id,
            reason="The answer was not correct yet. Retry this exercise before moving on.",
        )

    knowledge_state = list_skill_mastery(user_id)
    completed_exercise_ids = {
        attempt.exercise_id
        for attempt in list_attempt_history(user_id)
        if attempt.is_correct
    }
    next_exercise = next(
        (
            exercise
            for exercise in list_exercises_with_answers()
            if exercise["id"] not in completed_exercise_ids
            and exercise["id"] != exercise_id
            and knowledge_state.get(str(exercise["skill_id"]), 0) < 70
        ),
        None,
    )
    if next_exercise is None:
        return Recommendation(
            type="complete_goal",
            exercise_id=None,
            reason="All available seed exercises are complete enough for this MVP.",
        )

    level = classify_mastery(mastery)
    return Recommendation(
        type="next_exercise",
        exercise_id=str(next_exercise["id"]),
        reason=(
            f"Your mastery for {skill_id} is now {mastery}, classified as {level}. "
            "Continue with the next exercise."
        ),
    )
