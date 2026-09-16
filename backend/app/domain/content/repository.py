"""Content database access."""

from app.db.seed import EXERCISES, GOALS, TOPICS

_PRIVATE_EXERCISE_FIELDS = {
    "acceptable_answers",
    "expected_answer",
    "explanation",
    "incorrect_feedback",
    "solution",
}


def list_goals() -> list[dict]:
    return GOALS


def list_topics() -> list[dict]:
    return TOPICS


def list_exercises(
    topic_id: str | None = None,
    skill_id: str | None = None,
    difficulty: str | None = None,
) -> list[dict]:
    return [
        _public_exercise(exercise)
        for exercise in EXERCISES
        if _matches_filters(
            exercise=exercise,
            topic_id=topic_id,
            skill_id=skill_id,
            difficulty=difficulty,
        )
    ]


def get_public_exercise_by_id(exercise_id: str) -> dict | None:
    exercise = get_exercise_by_id(exercise_id)
    if exercise is None:
        return None
    return _public_exercise(exercise)


def get_exercise_by_id(exercise_id: str) -> dict | None:
    return next(
        (exercise for exercise in EXERCISES if exercise["id"] == exercise_id),
        None,
    )


def _public_exercise(exercise: dict) -> dict:
    return {key: value for key, value in exercise.items() if key not in _PRIVATE_EXERCISE_FIELDS}


def _matches_filters(
    exercise: dict,
    topic_id: str | None,
    skill_id: str | None,
    difficulty: str | None,
) -> bool:
    return (
        (topic_id is None or exercise["topic_id"] == topic_id)
        and (skill_id is None or exercise["skill_id"] == skill_id)
        and (difficulty is None or exercise["difficulty"] == difficulty)
    )
