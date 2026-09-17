"""My Learning persistence and course catalog access."""

from datetime import UTC, datetime

from app.core.database import SessionLocal, init_database
from app.db.models import UserCourseSelectionRecord

COURSE_CATALOG: list[dict] = [
    {
        "id": "python",
        "title": "Python Backend",
        "description": "FastAPI, API, databases, and backend foundation.",
        "status": "current",
        "goal_id": "goal_python_backend",
    },
    {
        "id": "ml",
        "title": "ML Engineer",
        "description": "Data, models, evaluation, and production ML workflow.",
        "status": "planned",
        "goal_id": None,
    },
    {
        "id": "cybersecurity",
        "title": "Cybersecurity",
        "description": "Web security, auth, threats, and secure backend basics.",
        "status": "planned",
        "goal_id": None,
    },
]


def list_courses() -> list[dict]:
    return [course.copy() for course in COURSE_CATALOG]


def get_course(course_id: str) -> dict | None:
    normalized_course_id = course_id.strip().lower()
    return next((course.copy() for course in COURSE_CATALOG if course["id"] == normalized_course_id), None)


def list_selected_course_records(user_id: str) -> list[UserCourseSelectionRecord]:
    init_database()
    with SessionLocal() as db:
        return (
            db.query(UserCourseSelectionRecord)
            .filter(UserCourseSelectionRecord.user_id == user_id)
            .order_by(UserCourseSelectionRecord.selected_at, UserCourseSelectionRecord.course_id)
            .all()
        )


def select_course(user_id: str, course_id: str) -> UserCourseSelectionRecord:
    init_database()
    normalized_course_id = course_id.strip().lower()
    with SessionLocal() as db:
        record = db.get(
            UserCourseSelectionRecord,
            {"user_id": user_id, "course_id": normalized_course_id},
        )
        if record is None:
            record = UserCourseSelectionRecord(
                user_id=user_id,
                course_id=normalized_course_id,
                selected_at=datetime.now(UTC),
            )
            db.add(record)
        db.commit()
        db.refresh(record)
        return record


def clear_selected_courses_for_tests() -> None:
    from app.core.database import reset_database_for_tests

    reset_database_for_tests()
