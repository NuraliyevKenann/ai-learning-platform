"""Registration and session endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_access_token, get_current_user
from app.domain.users.models import User
from app.domain.users.schemas import (
    AuthResponse,
    LoginRequest,
    LogoutResponse,
    RegisterRequest,
    UserResponse,
)
from app.domain.users.service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    login_user,
    logout_user,
    register_user,
    to_user_response,
)

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> AuthResponse:
    try:
        return register_user(payload.display_name, payload.email, payload.password)
    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(status_code=409, detail="Email is already registered.") from exc


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    try:
        return login_user(payload.email, payload.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail="Invalid email or password.") from exc


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)) -> UserResponse:
    return to_user_response(user)


@router.post("/logout", response_model=LogoutResponse)
def logout(
    token: str = Depends(get_access_token),
    _: User = Depends(get_current_user),
) -> LogoutResponse:
    logout_user(token)
    return LogoutResponse(status="ok")
