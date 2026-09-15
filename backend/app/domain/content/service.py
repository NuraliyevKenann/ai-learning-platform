"""Content business logic and read operations."""

from app.domain.content.repository import (
    list_exercises as list_exercises_from_repository,
)
from app.domain.content.repository import list_goals as list_goals_from_repository
from app.domain.content.repository import list_topics as list_topics_from_repository
from app.domain.content.schemas import Exercise, Goal, Topic


def list_goals() -> list[Goal]:
    return [Goal(**goal) for goal in list_goals_from_repository()]


def list_topics() -> list[Topic]:
    return [Topic(**topic) for topic in list_topics_from_repository()]


def list_exercises() -> list[Exercise]:
    return [Exercise(**exercise) for exercise in list_exercises_from_repository()]
