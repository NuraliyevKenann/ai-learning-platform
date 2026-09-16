from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_submit_attempt_updates_mastery_and_recommendation() -> None:
    client = TestClient(app)
    headers, _ = register_user(client)
    response = client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "exercise_id": "ex_python_variables_1",
        "is_correct": True,
        "score": 100.0,
        "old_mastery": 0.0,
        "new_mastery": 30.0,
        "recommendation": {
            "type": "next_exercise",
            "exercise_id": "ex_fastapi_health_1",
            "reason": (
                "Your mastery for skill_python_variables is now 30.0, "
                "classified as weak. Continue with the next exercise."
            ),
        },
    }


def test_submit_attempt_returns_404_for_unknown_exercise() -> None:
    client = TestClient(app)
    headers, _ = register_user(client)
    response = client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"exercise_id": "unknown_exercise", "answer": "x = 5"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found."}


def test_submit_attempt_accepts_equivalent_json_answer() -> None:
    client = TestClient(app)
    headers, _ = register_user(client)
    response = client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"exercise_id": "ex_fastapi_health_1", "answer": '{"status":"ok"}'},
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["new_mastery"] == 30.0


def test_submit_attempt_accepts_answer_with_different_spacing() -> None:
    client = TestClient(app)
    headers, _ = register_user(client)
    response = client.post(
        "/api/v1/attempts",
        headers=headers,
        json={"exercise_id": "ex_python_variables_1", "answer": "x=5"},
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["new_mastery"] == 30.0


def test_submit_attempt_requires_authentication() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x=5"},
    )
    assert response.status_code == 401
