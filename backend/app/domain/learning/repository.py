"""Learning database access."""

from app.core.database import SessionLocal, init_database
from app.db.models import KnowledgeStateRecord

_initial_knowledge_state: dict[str, float] = {
    "skill_python_variables": 0.0,
    "skill_fastapi_routes": 0.0,
}


def _ensure_state_exists(user_id: str) -> None:
    init_database()
    with SessionLocal() as db:
        existing_skill_ids = {
            skill_id
            for (skill_id,) in db.query(KnowledgeStateRecord.skill_id)
            .filter(KnowledgeStateRecord.user_id == user_id)
            .all()
        }
        for skill_id, mastery in _initial_knowledge_state.items():
            if skill_id not in existing_skill_ids:
                db.add(
                    KnowledgeStateRecord(
                        user_id=user_id,
                        skill_id=skill_id,
                        mastery=mastery,
                    )
                )
        db.commit()


def list_skill_mastery(user_id: str) -> dict[str, float]:
    _ensure_state_exists(user_id)
    with SessionLocal() as db:
        records = (
            db.query(KnowledgeStateRecord)
            .filter(KnowledgeStateRecord.user_id == user_id)
            .all()
        )
        mastery_by_skill_id = {record.skill_id: record.mastery for record in records}
        ordered_mastery = {
            skill_id: mastery_by_skill_id.get(skill_id, mastery)
            for skill_id, mastery in _initial_knowledge_state.items()
        }
        for skill_id, mastery in mastery_by_skill_id.items():
            if skill_id not in ordered_mastery:
                ordered_mastery[skill_id] = mastery
        return ordered_mastery


def get_mastery(user_id: str, skill_id: str) -> float:
    _ensure_state_exists(user_id)
    with SessionLocal() as db:
        record = db.get(KnowledgeStateRecord, {"user_id": user_id, "skill_id": skill_id})
        return record.mastery if record else 0.0


def set_mastery(user_id: str, skill_id: str, mastery: float) -> None:
    _ensure_state_exists(user_id)
    with SessionLocal() as db:
        record = db.get(KnowledgeStateRecord, {"user_id": user_id, "skill_id": skill_id})
        if record is None:
            record = KnowledgeStateRecord(user_id=user_id, skill_id=skill_id, mastery=mastery)
            db.add(record)
        else:
            record.mastery = mastery
        db.commit()


def reset_knowledge_state(user_id: str) -> None:
    init_database()
    with SessionLocal() as db:
        db.query(KnowledgeStateRecord).filter(KnowledgeStateRecord.user_id == user_id).delete()
        for skill_id, mastery in _initial_knowledge_state.items():
            db.add(KnowledgeStateRecord(user_id=user_id, skill_id=skill_id, mastery=mastery))
        db.commit()


def clear_all_knowledge_for_tests() -> None:
    from app.core.database import reset_database_for_tests

    reset_database_for_tests()
