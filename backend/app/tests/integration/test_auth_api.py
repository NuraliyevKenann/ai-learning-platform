from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_register_login_me_and_logout() -> None:
    client = TestClient(app)
    email = f"auth-{uuid4().hex}@example.com"
    register = client.post(
        "/api/v1/auth/register",
        json={"display_name": "Ada Learner", "email": email, "password": "strong-password"},
    )
    assert register.status_code == 201
    assert register.json()["user"]["email"] == email

    login = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "strong-password"},
    )
    assert login.status_code == 200
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["display_name"] == "Ada Learner"

    logout = client.post("/api/v1/auth/logout", headers=headers)
    assert logout.status_code == 200
    assert client.get("/api/v1/auth/me", headers=headers).status_code == 401


def test_duplicate_email_is_rejected() -> None:
    client = TestClient(app)
    email = f"duplicate-{uuid4().hex}@example.com"
    payload = {"display_name": "User", "email": email, "password": "strong-password"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_login_rejects_invalid_password() -> None:
    client = TestClient(app)
    email = f"invalid-{uuid4().hex}@example.com"
    client.post(
        "/api/v1/auth/register",
        json={"display_name": "User", "email": email, "password": "strong-password"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "wrong-password"},
    )
    assert response.status_code == 401
