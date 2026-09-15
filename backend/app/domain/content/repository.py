"""Content database access."""

from app.db.seed import EXERCISES, GOALS, TOPICS


def list_goals() -> list[dict]:
    return GOALS


def list_topics() -> list[dict]:
    return TOPICS


def list_exercises() -> list[dict]:
    return [
        {key: value for key, value in exercise.items() if key != "expected_answer"}
        for exercise in EXERCISES
    ]


def get_exercise_by_id(exercise_id: str) -> dict | None:
    return next(
        (exercise for exercise in EXERCISES if exercise["id"] == exercise_id),
        None,
    )
