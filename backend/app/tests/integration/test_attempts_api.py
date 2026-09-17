from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_submit_attempt_updates_mastery_and_recommendation() -> None:
    client = TestClient(app)
    register_user(client)
    response = client.post(
        "/api/v1/attempts",
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
        "feedback": "Correct. Review the explanation, then continue with the recommendation.",
        "hint": None,
        "solution": "x = 5",
        "explanation": "A variable stores a value under a name. Here, x becomes a name for the number 5.",
        "recommendation": {
            "type": "next_exercise",
            "exercise_id": "ex_python_variables_2",
            "reason": (
                "Your mastery for skill_python_variables is now 30.0, "
                "classified as weak. Continue with the next exercise."
            ),
        },
    }


def test_recommendation_skips_exercises_already_answered_correctly() -> None:
    client = TestClient(app)
    register_user(client)

    first_response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )
    assert first_response.status_code == 200
    assert first_response.json()["recommendation"]["exercise_id"] == "ex_python_variables_2"

    second_response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_2", "answer": "score = 10\nscore = 15"},
    )

    assert second_response.status_code == 200
    assert second_response.json()["recommendation"]["exercise_id"] == "ex_http_api_basics_1"


def test_submit_attempt_returns_404_for_unknown_exercise() -> None:
    client = TestClient(app)
    register_user(client)
    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "unknown_exercise", "answer": "x = 5"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found."}


def test_submit_attempt_accepts_equivalent_json_answer() -> None:
    client = TestClient(app)
    register_user(client)
    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_fastapi_health_1", "answer": '{"status":"ok"}'},
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["new_mastery"] == 30.0


def test_submit_attempt_accepts_answer_with_different_spacing() -> None:
    client = TestClient(app)
    register_user(client)
    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x=5"},
    )
    assert response.status_code == 200
    assert response.json()["is_correct"] is True
    assert response.json()["new_mastery"] == 30.0



def test_submit_attempt_accepts_fastapi_decorator_variants() -> None:
    client = TestClient(app)
    register_user(client)

    for answer in [
        '@app.get("/api/v1/health")',
        "@app.get('/api/v1/health')",
        'app.get("/api/v1/health")',
        '@app.get( \u201c/api/v1/health\u201d )',
        '```python\n@app.get("/api/v1/health")\n```',
    ]:
        response = client.post(
            "/api/v1/attempts",
            json={"exercise_id": "ex_fastapi_routes_2", "answer": answer},
        )
        assert response.status_code == 200
        assert response.json()["is_correct"] is True

def test_submit_attempt_returns_hint_and_solution_for_wrong_answer() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_http_api_basics_1", "answer": "POST"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["is_correct"] is False
    assert body["feedback"] == "For reading data, use GET. POST is usually for creating or submitting data."
    assert body["hint"] == "Think about the method browsers use when opening a page URL."
    assert body["solution"] == "GET"
    assert body["explanation"] == "GET is normally used for safe read operations, like listing goals or exercises."


def test_submit_attempt_requires_authentication() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x=5"},
    )
    assert response.status_code == 401


def test_attempt_history_lists_current_users_attempts() -> None:
    client = TestClient(app)
    register_user(client)
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "wrong"},
    )
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )

    response = client.get("/api/v1/attempts/history")

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 2
    assert items[0]["exercise_id"] == "ex_python_variables_1"
    assert items[0]["answer"] == "x = 5"
    assert items[0]["is_correct"] is True
    assert items[0]["old_mastery"] == 0.0
    assert items[0]["new_mastery"] == 30.0
    assert items[1]["answer"] == "wrong"
    assert items[1]["is_correct"] is False


def test_attempt_history_can_be_limited() -> None:
    client = TestClient(app)
    register_user(client)
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "wrong"},
    )
    client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )

    response = client.get("/api/v1/attempts/history?limit=1")

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["answer"] == "x = 5"


def test_attempt_history_is_isolated_between_users() -> None:
    first_client = TestClient(app)
    second_client = TestClient(app)
    register_user(first_client, "First User")
    register_user(second_client, "Second User")
    first_client.post(
        "/api/v1/attempts",
        json={"exercise_id": "ex_python_variables_1", "answer": "x = 5"},
    )

    response = second_client.get("/api/v1/attempts/history")

    assert response.status_code == 200
    assert response.json() == {"items": []}


def test_attempt_history_requires_authentication() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/attempts/history")
    assert response.status_code == 401
