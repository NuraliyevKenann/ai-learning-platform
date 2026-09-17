from fastapi.testclient import TestClient

from app.main import app


def test_list_exercises_returns_public_learning_fields_only() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/exercises")

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) == 22
    assert items[0] == {
        "id": "ex_python_variables_1",
        "topic_id": "topic_python_variables",
        "skill_id": "skill_python_variables",
        "title": "Create your first variable",
        "prompt": "Create a variable named x with the value 5.",
        "difficulty": "easy",
        "estimated_minutes": 2,
        "hint": "Use the assignment operator = between the variable name and the value.",
    }
    assert "expected_answer" not in items[0]
    assert "solution" not in items[0]


def test_list_exercises_can_filter_by_topic_and_difficulty() -> None:
    client = TestClient(app)

    response = client.get(
        "/api/v1/exercises",
        params={"topic_id": "topic_fastapi_routes", "difficulty": "medium"},
    )

    assert response.status_code == 200
    assert [item["id"] for item in response.json()["items"]] == ["ex_fastapi_routes_2"]


def test_read_exercise_returns_one_public_exercise() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/exercises/ex_database_basics_1")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == "ex_database_basics_1"
    assert body["hint"] == "Use SELECT * when you want all columns from a table."
    assert "expected_answer" not in body
    assert "solution" not in body


def test_read_exercise_returns_404_for_unknown_exercise() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/exercises/unknown")

    assert response.status_code == 404
    assert response.json() == {"detail": "Exercise not found."}
