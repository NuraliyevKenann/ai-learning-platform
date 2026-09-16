"""Registration and session endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import get_current_user, get_session_token
from app.core.config import settings
from app.domain.users.models import User
from app.domain.users.schemas import (
    AuthResponse,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    UpdateProfileRequest,
    UserResponse,
)
from app.domain.users.service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    login_user,
    logout_user,
    register_user,
    to_user_response,
    update_profile,
)

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, response: Response) -> AuthResponse:
    try:
        result = register_user(payload.display_name, payload.email, payload.password)
        _set_session_cookie(response, result.token)
        return result.response
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=409, detail="Email is already registered.") from exc


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, response: Response) -> AuthResponse:
    try:
        result = login_user(payload.email, payload.password)
        _set_session_cookie(response, result.token)
        return result.response
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail="Invalid email or password.") from exc


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return to_user_response(user)


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UpdateProfileRequest,
    user: User = Depends(get_current_user),
) -> UserResponse:
    return update_profile(user.id, payload.display_name)


@router.post("/logout", response_model=LogoutResponse)
def logout(
    response: Response,
    token: str = Depends(get_session_token),
    _: User = Depends(get_current_user),
) -> LogoutResponse:
    logout_user(token)
    response.delete_cookie(
        key=settings.session_cookie_name,
        path=settings.api_v1_prefix,
        secure=settings.session_cookie_secure,
        httponly=True,
        samesite="lax",
    )
    return LogoutResponse(status="ok")


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_max_age_seconds,
        path=settings.api_v1_prefix,
        secure=settings.session_cookie_secure,
        httponly=True,
        samesite="lax",
    )
