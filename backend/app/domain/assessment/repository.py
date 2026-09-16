"""Assessment database access."""

from datetime import UTC, datetime

from app.core.database import SessionLocal, init_database
from app.db.models import AttemptRecord
from app.domain.assessment.schemas import AttemptHistoryItem


def record_attempt(
    user_id: str,
    exercise_id: str,
    answer: str,
    is_correct: bool,
    score: float,
    old_mastery: float,
    new_mastery: float,
) -> None:
    init_database()
    with SessionLocal() as db:
        db.add(
            AttemptRecord(
                user_id=user_id,
                exercise_id=exercise_id,
                answer=answer,
                is_correct=is_correct,
                score=score,
                old_mastery=old_mastery,
                new_mastery=new_mastery,
                created_at=datetime.now(UTC),
            )
        )
        db.commit()


def list_attempt_history(user_id: str, limit: int | None = None) -> list[AttemptHistoryItem]:
    init_database()
    with SessionLocal() as db:
        query = (
            db.query(AttemptRecord)
            .filter(AttemptRecord.user_id == user_id)
            .order_by(AttemptRecord.created_at.desc(), AttemptRecord.id.desc())
        )
        if limit is not None:
            query = query.limit(limit)
        records = query.all()
        return [
            AttemptHistoryItem(
                id=record.id,
                exercise_id=record.exercise_id,
                answer=record.answer,
                is_correct=record.is_correct,
                score=record.score,
                old_mastery=record.old_mastery,
                new_mastery=record.new_mastery,
                created_at=record.created_at,
            )
            for record in records
        ]
