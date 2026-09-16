from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_reset_knowledge_state_returns_mastery_to_zero() -> None:
    client = TestClient(app)
    headers, user = register_user(client)
    client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    response = client.post("/api/v1/knowledge/reset", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "items": [
            {"user_id": user["id"], "skill_id": "skill_python_variables", "mastery": 0.0, "level": "weak"},
            {"user_id": user["id"], "skill_id": "skill_fastapi_routes", "mastery": 0.0, "level": "weak"},
        ],
    }


def test_progress_is_isolated_between_users() -> None:
    client = TestClient(app)
    first_headers, _ = register_user(client, "First User")
    second_headers, _ = register_user(client, "Second User")
    client.post(
        "/api/v1/attempts",
        headers=first_headers,
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    first_state = client.get("/api/v1/knowledge/state", headers=first_headers).json()
    second_state = client.get("/api/v1/knowledge/state", headers=second_headers).json()
    assert first_state["items"][0]["mastery"] == 30.0
    assert second_state["items"][0]["mastery"] == 0.0
