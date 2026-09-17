from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_current_recommendation_starts_with_first_exercise() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.get("/api/v1/recommendations/current")

    assert response.status_code == 200
    assert response.json() == {
        "recommendation": {
            "type": "start_exercise",
            "exercise_id": "ex_python_variables_1",
            "reason": "Start with Python variables because they are the first prerequisite.",
        }
    }


def test_current_recommendation_updates_after_attempt() -> None:
    client = TestClient(app)
    register_user(client)

    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    response = client.get("/api/v1/recommendations/current")

    assert response.status_code == 200
    assert response.json()["recommendation"]["type"] == "next_exercise"
    assert response.json()["recommendation"]["exercise_id"] == "ex_python_variables_2"


def test_current_recommendation_resets_with_knowledge_state() -> None:
    client = TestClient(app)
    register_user(client)

    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    client.post("/api/v1/knowledge/reset")
    response = client.get("/api/v1/recommendations/current")

    assert response.status_code == 200
    assert response.json()["recommendation"]["type"] == "start_exercise"
    assert response.json()["recommendation"]["exercise_id"] == "ex_python_variables_1"


def test_current_recommendation_is_isolated_between_users() -> None:
    first_client = TestClient(app)
    second_client = TestClient(app)
    register_user(first_client, "First User")
    register_user(second_client, "Second User")

    first_client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    second_response = second_client.get("/api/v1/recommendations/current")

    assert second_response.status_code == 200
    assert second_response.json()["recommendation"]["type"] == "start_exercise"
    assert second_response.json()["recommendation"]["exercise_id"] == "ex_python_variables_1"
