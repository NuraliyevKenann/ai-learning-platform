"""Content business logic and read operations."""

from app.domain.content.repository import get_public_exercise_by_id
from app.domain.content.repository import (
    list_exercises as list_exercises_from_repository,
)
from app.domain.content.repository import list_goals as list_goals_from_repository
from app.domain.content.repository import list_topics as list_topics_from_repository
from app.domain.assessment.repository import list_attempt_history
from app.domain.content.schemas import (
    Exercise,
    ExerciseProgressItem,
    ExerciseProgressResponse,
    ExerciseProgressSummary,
    Goal,
    Topic,
)
from app.domain.recommendations.service import get_current_recommendation


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



def get_exercise_progress(user_id: str) -> ExerciseProgressResponse:
    exercises = list_exercises_from_repository()
    attempts = list_attempt_history(user_id)
    recommendation = get_current_recommendation(user_id)
    recommended_exercise_id = recommendation.exercise_id

    attempts_by_exercise_id: dict[str, list] = {}
    for attempt in attempts:
        attempts_by_exercise_id.setdefault(attempt.exercise_id, []).append(attempt)

    items: list[ExerciseProgressItem] = []
    for exercise in exercises:
        exercise_id = str(exercise["id"])
        exercise_attempts = attempts_by_exercise_id.get(exercise_id, [])
        attempts_count = len(exercise_attempts)
        last_attempt = exercise_attempts[0] if exercise_attempts else None
        best_score = max((attempt.score for attempt in exercise_attempts), default=None)
        is_completed = any(attempt.is_correct for attempt in exercise_attempts)
        is_recommended = exercise_id == recommended_exercise_id

        if is_completed:
            status = "completed"
        elif is_recommended:
            status = "current"
        else:
            status = "available"

        items.append(
            ExerciseProgressItem(
                exercise_id=exercise_id,
                status=status,
                is_recommended=is_recommended,
                attempts_count=attempts_count,
                last_score=last_attempt.score if last_attempt else None,
                best_score=best_score,
            )
        )

    completed = sum(1 for item in items if item.status == "completed")
    current = sum(1 for item in items if item.status == "current")
    total = len(items)
    return ExerciseProgressResponse(
        items=items,
        summary=ExerciseProgressSummary(
            total=total,
            completed=completed,
            current=current,
            remaining=max(total - completed, 0),
        ),
    )
