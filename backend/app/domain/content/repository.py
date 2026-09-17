"""Content database access."""

from app.core.database import SessionLocal, init_database
from app.db.models import ExerciseRecord, GoalRecord, TopicRecord
from app.db.seed import EXERCISES, GOALS, TOPICS

_PRIVATE_EXERCISE_FIELDS = {
    "acceptable_answers",
    "expected_answer",
    "explanation",
    "incorrect_feedback",
    "solution",
}


def list_goals() -> list[dict]:
    _ensure_seed_content()
    with SessionLocal() as db:
        records = db.query(GoalRecord).order_by(GoalRecord.id).all()
        return [_goal_to_dict(record) for record in records]


def list_topics() -> list[dict]:
    _ensure_seed_content()
    with SessionLocal() as db:
        records = db.query(TopicRecord).order_by(TopicRecord.order, TopicRecord.id).all()
        return [_topic_to_dict(record) for record in records]


def list_exercises(
    topic_id: str | None = None,
    skill_id: str | None = None,
    difficulty: str | None = None,
) -> list[dict]:
    return [
        _public_exercise(exercise)
        for exercise in list_exercises_with_answers()
        if _matches_filters(
            exercise=exercise,
            topic_id=topic_id,
            skill_id=skill_id,
            difficulty=difficulty,
        )
    ]


def list_exercises_with_answers() -> list[dict]:
    _ensure_seed_content()
    return sorted((exercise.copy() for exercise in EXERCISES), key=lambda item: int(item["order"]))


def get_public_exercise_by_id(exercise_id: str) -> dict | None:
    exercise = get_exercise_by_id(exercise_id)
    if exercise is None:
        return None
    return _public_exercise(exercise)


def get_exercise_by_id(exercise_id: str) -> dict | None:
    return next(
        (exercise for exercise in list_exercises_with_answers() if exercise["id"] == exercise_id),
        None,
    )


def _ensure_seed_content() -> None:
    init_database()
    with SessionLocal() as db:
        for goal in GOALS:
            db.merge(GoalRecord(**goal))
        db.commit()
        for topic in TOPICS:
            db.merge(TopicRecord(**topic))
        db.commit()
        for exercise in EXERCISES:
            db.merge(
                ExerciseRecord(
                    id=exercise["id"],
                    topic_id=exercise["topic_id"],
                    skill_id=exercise["skill_id"],
                    prompt=exercise["prompt"],
                    expected_answer=exercise["expected_answer"],
                    difficulty=exercise["difficulty"],
                    order=exercise["order"],
                )
            )
        db.commit()


def _goal_to_dict(record: GoalRecord) -> dict:
    return {
        "id": record.id,
        "title": record.title,
        "description": record.description,
    }


def _topic_to_dict(record: TopicRecord) -> dict:
    return {
        "id": record.id,
        "goal_id": record.goal_id,
        "title": record.title,
        "skill_id": record.skill_id,
        "order": record.order,
    }


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
