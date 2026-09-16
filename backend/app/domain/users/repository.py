"""In-memory user and session storage for the authentication MVP."""

import secrets
from dataclasses import dataclass, replace
from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.domain.users.models import User


@dataclass(frozen=True)
class Session:
    user_id: str
    expires_at: datetime


_users_by_id: dict[str, User] = {}
_user_id_by_email: dict[str, str] = {}
_sessions: dict[str, Session] = {}


def create_user(user: User) -> None:
    _users_by_id[user.id] = user
    _user_id_by_email[user.email] = user.id


def get_user_by_id(user_id: str) -> User | None:
    return _users_by_id.get(user_id)


def get_user_by_email(email: str) -> User | None:
    user_id = _user_id_by_email.get(email.strip().lower())
    return _users_by_id.get(user_id) if user_id else None


def update_user_display_name(user_id: str, display_name: str) -> User | None:
    user = get_user_by_id(user_id)
    if user is None:
        return None
    updated_user = replace(user, display_name=display_name)
    _users_by_id[user_id] = updated_user
    return updated_user


def create_session(user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = Session(
        user_id=user_id,
        expires_at=datetime.now(UTC) + timedelta(seconds=settings.session_max_age_seconds),
    )
    return token


def get_user_by_session(token: str) -> User | None:
    session = _sessions.get(token)
    if session is None:
        return None
    if session.expires_at <= datetime.now(UTC):
        delete_session(token)
        return None
    return get_user_by_id(session.user_id)


def delete_session(token: str) -> None:
    _sessions.pop(token, None)


def clear_users_for_tests() -> None:
    _users_by_id.clear()
    _user_id_by_email.clear()
    _sessions.clear()
