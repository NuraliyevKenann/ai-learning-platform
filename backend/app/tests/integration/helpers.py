from uuid import uuid4

from fastapi.testclient import TestClient


def register_user(client: TestClient, display_name: str = "Test User") -> tuple[dict[str, str], dict]:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "display_name": display_name,
            "email": f"test-{uuid4().hex}@example.com",
            "password": "secure-password-123",
        },
    )
    assert response.status_code == 201
    body = response.json()
    return {"Authorization": f"Bearer {body['access_token']}"}, body["user"]
