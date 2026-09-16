"""Shared FastAPI dependencies."""

from fastapi import Cookie, Depends, HTTPException, status

from app.core.config import settings
from app.domain.users.models import User
from app.domain.users.service import authenticate_token

def get_session_token(
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> str:
    if session_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    return session_token


def get_current_user(token: str = Depends(get_session_token)) -> User:
    user = authenticate_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired.",
        )
    return user
