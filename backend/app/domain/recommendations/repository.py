"""Recommendation database access."""

from datetime import UTC, datetime

from app.core.database import SessionLocal, init_database
from app.db.models import CurrentRecommendationRecord

_initial_recommendation: dict[str, str | None] = {
    "type": "start_exercise",
    "exercise_id": "ex_python_variables_1",
    "reason": "Start with Python variables because they are the first prerequisite.",
}


def _record_to_dict(record: CurrentRecommendationRecord) -> dict[str, str | None]:
    return {
        "type": record.type,
        "exercise_id": record.exercise_id,
        "reason": record.reason,
    }


def _create_initial_recommendation(user_id: str) -> CurrentRecommendationRecord:
    return CurrentRecommendationRecord(
        user_id=user_id,
        type=str(_initial_recommendation["type"]),
        exercise_id=_initial_recommendation["exercise_id"],
        reason=str(_initial_recommendation["reason"]),
        updated_at=datetime.now(UTC),
    )


def get_current_recommendation(user_id: str) -> dict[str, str | None]:
    init_database()
    with SessionLocal() as db:
        record = db.get(CurrentRecommendationRecord, user_id)
        if record is None:
            record = _create_initial_recommendation(user_id)
            db.add(record)
            db.commit()
            db.refresh(record)
        return _record_to_dict(record)


def set_current_recommendation(user_id: str, recommendation: dict[str, str | None]) -> None:
    init_database()
    with SessionLocal() as db:
        record = db.get(CurrentRecommendationRecord, user_id)
        if record is None:
            record = CurrentRecommendationRecord(user_id=user_id, updated_at=datetime.now(UTC))
            db.add(record)
        record.type = str(recommendation["type"])
        record.exercise_id = recommendation["exercise_id"]
        record.reason = str(recommendation["reason"])
        record.updated_at = datetime.now(UTC)
        db.commit()


def reset_current_recommendation(user_id: str) -> None:
    set_current_recommendation(user_id, _initial_recommendation)


def clear_all_recommendations_for_tests() -> None:
    init_database()
    with SessionLocal() as db:
        db.query(CurrentRecommendationRecord).delete()
        db.commit()
