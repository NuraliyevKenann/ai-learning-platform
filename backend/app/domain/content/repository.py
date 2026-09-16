"""Content database access."""

from app.db.seed import EXERCISES, GOALS, TOPICS
from app.core.database import SessionLocal, init_database
from app.db.models import ExerciseRecord, GoalRecord, TopicRecord


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


def list_exercises() -> list[dict]:
    return [_public_exercise(exercise) for exercise in list_exercises_with_answers()]


def list_exercises_with_answers() -> list[dict]:
    _ensure_seed_content()
    with SessionLocal() as db:
        records = db.query(ExerciseRecord).order_by(ExerciseRecord.order, ExerciseRecord.id).all()
        return [_exercise_to_dict(record) for record in records]


def get_exercise_by_id(exercise_id: str) -> dict | None:
    _ensure_seed_content()
    with SessionLocal() as db:
        record = db.get(ExerciseRecord, exercise_id)
        return _exercise_to_dict(record) if record else None


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
            db.merge(ExerciseRecord(**exercise))
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


def _exercise_to_dict(record: ExerciseRecord) -> dict:
    return {
        "id": record.id,
        "topic_id": record.topic_id,
        "skill_id": record.skill_id,
        "prompt": record.prompt,
        "expected_answer": record.expected_answer,
        "difficulty": record.difficulty,
        "order": record.order,
    }


def _public_exercise(exercise: dict) -> dict:
    return {key: value for key, value in exercise.items() if key != "expected_answer"}
