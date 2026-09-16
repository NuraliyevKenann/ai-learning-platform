"""User and session persistence."""

import secrets
from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.core.database import SessionLocal, init_database
from app.db.models import SessionRecord, UserRecord
from app.domain.users.models import User


def _to_domain(record: UserRecord) -> User:
    return User(
        id=record.id,
        email=record.email,
        display_name=record.display_name,
        password_hash=record.password_hash,
        created_at=record.created_at,
    )


def create_user(user: User) -> None:
    init_database()
    with SessionLocal() as db:
        db.add(
            UserRecord(
                id=user.id,
                email=user.email,
                display_name=user.display_name,
                password_hash=user.password_hash,
                created_at=user.created_at,
            )
        )
        db.commit()


def get_user_by_id(user_id: str) -> User | None:
    init_database()
    with SessionLocal() as db:
        record = db.get(UserRecord, user_id)
        return _to_domain(record) if record else None


def get_user_by_email(email: str) -> User | None:
    init_database()
    with SessionLocal() as db:
        record = db.query(UserRecord).filter(UserRecord.email == email.strip().lower()).one_or_none()
        return _to_domain(record) if record else None


def update_user_display_name(user_id: str, display_name: str) -> User | None:
    init_database()
    with SessionLocal() as db:
        record = db.get(UserRecord, user_id)
        if record is None:
            return None
        record.display_name = display_name
        db.commit()
        db.refresh(record)
        return _to_domain(record)


def create_session(user_id: str) -> str:
    init_database()
    token = secrets.token_urlsafe(32)
    with SessionLocal() as db:
        db.add(
            SessionRecord(
                token=token,
                user_id=user_id,
                expires_at=datetime.now(UTC) + timedelta(seconds=settings.session_max_age_seconds),
            )
        )
        db.commit()
    return token


def get_user_by_session(token: str) -> User | None:
    init_database()
    with SessionLocal() as db:
        session = db.get(SessionRecord, token)
        if session is None:
            return None
        expires_at = session.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= datetime.now(UTC):
            db.delete(session)
            db.commit()
            return None
        record = db.get(UserRecord, session.user_id)
        return _to_domain(record) if record else None


def delete_session(token: str) -> None:
    init_database()
    with SessionLocal() as db:
        session = db.get(SessionRecord, token)
        if session is not None:
            db.delete(session)
            db.commit()


def clear_users_for_tests() -> None:
    from app.core.database import reset_database_for_tests

    reset_database_for_tests()
