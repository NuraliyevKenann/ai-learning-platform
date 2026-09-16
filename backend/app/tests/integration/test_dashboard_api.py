from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_dashboard_summary_requires_authentication() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401


def test_dashboard_summary_combines_user_progress_recommendation_and_attempts() -> None:
    client = TestClient(app)
    user = register_user(client, "Dashboard User")
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "wrong"},
    )
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["user"]["id"] == user["id"]
    assert body["goal"]["id"] == "goal_python_backend"
    assert body["current_exercise"]["id"] == "ex_fastapi_health_1"
    assert body["current_recommendation"]["type"] == "next_exercise"
    assert body["average_mastery"] == 15
    assert body["completed_skills"] == 0
    assert body["total_skills"] == 2
    assert body["total_attempts"] == 2
    assert body["correct_attempts"] == 1
    assert len(body["knowledge"]) == 2
    assert len(body["recent_attempts"]) == 2
    assert body["recent_attempts"][0]["answer"] == "x = 5"
    assert body["recent_attempts"][1]["answer"] == "wrong"


def test_dashboard_summary_limits_recent_attempts() -> None:
    client = TestClient(app)
    register_user(client)
    for answer in ["wrong-1", "wrong-2", "wrong-3", "wrong-4", "wrong-5"]:
        client.post(
            "/api/v1/attempts",
            json={"exercise_id": "ex_python_variables_1", "answer": answer},
        )

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["total_attempts"] == 5
    assert len(body["recent_attempts"]) == 4
    assert body["recent_attempts"][0]["answer"] == "wrong-5"


def test_dashboard_summary_is_isolated_between_users() -> None:
    first_client = TestClient(app)
    second_client = TestClient(app)
    register_user(first_client, "First User")
    register_user(second_client, "Second User")
    first_client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )

    response = second_client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["average_mastery"] == 0
    assert body["total_attempts"] == 0
    assert body["recent_attempts"] == []
