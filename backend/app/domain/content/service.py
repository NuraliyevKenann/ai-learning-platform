"""Content business logic and read operations."""

from app.domain.content.repository import get_public_exercise_by_id
from app.domain.content.repository import (
    list_exercises as list_exercises_from_repository,
)
from app.domain.content.repository import list_goals as list_goals_from_repository
from app.domain.content.repository import list_topics as list_topics_from_repository
from app.domain.content.schemas import Exercise, Goal, Topic


class ExerciseNotFoundError(Exception):
    """Raised when an exercise is not found in the content catalog."""


def list_goals() -> list[Goal]:
    return [Goal(**goal) for goal in list_goals_from_repository()]


def list_topics() -> list[Topic]:
    return [Topic(**topic) for topic in list_topics_from_repository()]


def list_exercises(
    topic_id: str | None = None,
    skill_id: str | None = None,
    difficulty: str | None = None,
) -> list[Exercise]:
    return [
        Exercise(**exercise)
        for exercise in list_exercises_from_repository(
            topic_id=topic_id,
            skill_id=skill_id,
            difficulty=difficulty,
        )
    ]


def get_exercise(exercise_id: str) -> Exercise:
    exercise = get_public_exercise_by_id(exercise_id)
    if exercise is None:
        raise ExerciseNotFoundError
    return Exercise(**exercise)
