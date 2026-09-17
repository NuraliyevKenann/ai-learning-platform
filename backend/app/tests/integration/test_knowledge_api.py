from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_reset_knowledge_state_returns_mastery_to_zero() -> None:
    client = TestClient(app)
    user = register_user(client)
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    response = client.post("/api/v1/knowledge/reset")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert len(body["items"]) == 12
    assert body["items"][0] == {
        "user_id": user["id"],
        "skill_id": "skill_python_variables",
        "mastery": 0.0,
        "level": "weak",
    }
    assert body["items"][-1] == {
        "user_id": user["id"],
        "skill_id": "skill_api_errors",
        "mastery": 0.0,
        "level": "weak",
    }
    assert all(item["mastery"] == 0.0 for item in body["items"])


def test_progress_is_isolated_between_users() -> None:
    first_client = TestClient(app)
    second_client = TestClient(app)
    register_user(first_client, "First User")
    register_user(second_client, "Second User")
    first_client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    first_state = first_client.get("/api/v1/knowledge/state").json()
    second_state = second_client.get("/api/v1/knowledge/state").json()
    assert first_state["items"][0]["mastery"] == 30.0
    assert second_state["items"][0]["mastery"] == 0.0
