"""In-memory user and session storage for the authentication MVP."""

import secrets

from app.domain.users.models import User

_users_by_id: dict[str, User] = {}
_user_id_by_email: dict[str, str] = {}
_sessions: dict[str, str] = {}


def create_user(user: User) -> None:
    _users_by_id[user.id] = user
    _user_id_by_email[user.email] = user.id


def get_user_by_id(user_id: str) -> User | None:
    return _users_by_id.get(user_id)


def get_user_by_email(email: str) -> User | None:
    user_id = _user_id_by_email.get(email.strip().lower())
    return _users_by_id.get(user_id) if user_id else None


def create_session(user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = user_id
    return token


def get_user_by_session(token: str) -> User | None:
    user_id = _sessions.get(token)
    return get_user_by_id(user_id) if user_id else None


def delete_session(token: str) -> None:
    _sessions.pop(token, None)


def clear_users_for_tests() -> None:
    _users_by_id.clear()
    _user_id_by_email.clear()
    _sessions.clear()
