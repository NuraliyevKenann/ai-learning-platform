"""Assessment database access."""

from datetime import UTC, datetime

from app.core.database import SessionLocal, init_database
from app.db.models import AttemptRecord


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
