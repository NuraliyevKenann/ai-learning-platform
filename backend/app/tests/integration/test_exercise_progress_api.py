from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_exercise_progress_requires_authentication() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/exercises/progress")

    assert response.status_code == 401


def test_exercise_progress_starts_with_first_exercise_as_current() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.get("/api/v1/exercises/progress")

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == {"total": 6, "completed": 0, "current": 1, "remaining": 6}
    assert body["items"][0] == {
        "exercise_id": "ex_python_variables_1",
        "status": "current",
        "is_recommended": True,
        "attempts_count": 0,
        "last_score": None,
        "best_score": None,
    }
    assert body["items"][1]["status"] == "available"


def test_exercise_progress_marks_completed_and_current_exercises() -> None:
    client = TestClient(app)
    register_user(client)
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_2", "answer": "wrong"},
    )

    response = client.get("/api/v1/exercises/progress")

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == {"total": 6, "completed": 1, "current": 1, "remaining": 5}
    first, second = body["items"][0], body["items"][1]
    assert first["status"] == "completed"
    assert first["attempts_count"] == 1
    assert first["best_score"] == 100.0
    assert second["status"] == "current"
    assert second["is_recommended"] is True
    assert second["attempts_count"] == 1
    assert second["last_score"] == 0.0
    assert second["best_score"] == 0.0
