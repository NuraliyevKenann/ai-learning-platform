from fastapi.testclient import TestClient

from app.main import app


def test_content_api_returns_seeded_learning_path_from_database() -> None:
    client = TestClient(app)

    goals = client.get("/api/v1/goals")
    topics = client.get("/api/v1/topics")
    exercises = client.get("/api/v1/exercises")

    assert goals.status_code == 200
    assert topics.status_code == 200
    assert exercises.status_code == 200
    assert goals.json()["items"][0]["id"] == "goal_python_backend"
    assert len(topics.json()["items"]) == 12
    assert len(exercises.json()["items"]) == 22
    assert exercises.json()["items"][0]["id"] == "ex_python_variables_1"
    assert exercises.json()["items"][1]["id"] == "ex_python_variables_2"
    assert "expected_answer" not in exercises.json()["items"][0]
