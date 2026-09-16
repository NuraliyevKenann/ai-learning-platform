"""User registration, login, and session logic."""

from datetime import UTC, datetime
from uuid import uuid4

from app.core.security import hash_password, verify_password
from app.domain.users.models import User
from app.domain.users.repository import (
    create_session,
    create_user,
    delete_session,
    get_user_by_email,
    get_user_by_session,
)
from app.domain.users.schemas import AuthResponse, UserResponse


class EmailAlreadyRegisteredError(Exception):
    """Raised when registration uses an existing email."""


class InvalidCredentialsError(Exception):
    """Raised when an email/password pair cannot be authenticated."""


def register_user(display_name: str, email: str, password: str) -> AuthResponse:
    normalized_email = email.strip().lower()
    if get_user_by_email(normalized_email):
        raise EmailAlreadyRegisteredError

    user = User(
        id=f"user_{uuid4().hex}",
        email=normalized_email,
        display_name=display_name,
        password_hash=hash_password(password),
        created_at=datetime.now(UTC),
    )
    create_user(user)
    return _build_auth_response(user)


def login_user(email: str, password: str) -> AuthResponse:
    user = get_user_by_email(email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError
    return _build_auth_response(user)


def authenticate_token(token: str) -> User | None:
    return get_user_by_session(token)


def logout_user(token: str) -> None:
    delete_session(token)


def to_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        created_at=user.created_at,
    )


def _build_auth_response(user: User) -> AuthResponse:
    return AuthResponse(access_token=create_session(user.id), user=to_user_response(user))
