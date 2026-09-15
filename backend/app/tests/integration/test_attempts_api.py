from fastapi.testclient import TestClient

from app.domain.learning.repository import reset_knowledge_state
from app.domain.recommendations.repository import reset_current_recommendation
from app.main import app


def test_submit_attempt_updates_mastery_and_recommendation() -> None:
    reset_knowledge_state()
    reset_current_recommendation()

    client = TestClient(app)

    response = client.post(
        "/api/v1/attempts",
        json={
            "exercise_id": "ex_python_variables_1",
            "answer": "x = 5",
        },
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
    reset_knowledge_state()
    reset_current_recommendation()

    client = TestClient(app)

    response = client.post(
        "/api/v1/attempts",
        json={
            "exercise_id": "unknown_exercise",
            "answer": "x = 5",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found."}


def test_submit_attempt_accepts_equivalent_json_answer() -> None:
    reset_knowledge_state()
    reset_current_recommendation()

    client = TestClient(app)

    response = client.post(
        "/api/v1/attempts",
        json={
            "exercise_id": "ex_fastapi_health_1",
            "answer": '{"status":"ok"}',
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["is_correct"] is True
    assert body["new_mastery"] == 30.0


def test_submit_attempt_accepts_answer_with_different_spacing() -> None:
    reset_knowledge_state()
    reset_current_recommendation()

    client = TestClient(app)

    response = client.post(
        "/api/v1/attempts",
        json={
            "exercise_id": "ex_python_variables_1",
            "answer": "x=5",
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["is_correct"] is True
    assert body["new_mastery"] == 30.0
