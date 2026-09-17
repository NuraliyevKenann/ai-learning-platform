from fastapi.testclient import TestClient

from app.main import app
from app.tests.integration.helpers import register_user


def test_my_learning_requires_authentication() -> None:
    client = TestClient(app)

    response = client.get("/api/v1/my-learning")

    assert response.status_code == 401


def test_authenticated_user_can_list_available_courses() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.get("/api/v1/my-learning/courses")

    assert response.status_code == 200
    body = response.json()
    assert [course["id"] for course in body["items"]] == ["python", "ml", "cybersecurity"]
    assert body["items"][0]["selected"] is False


def test_user_can_select_course_for_my_learning() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.post("/api/v1/my-learning/courses", json={"course_id": "python"})

    assert response.status_code == 200
    body = response.json()
    assert body["active_course"]["id"] == "python"
    assert body["active_course"]["selected"] is True
    assert body["selected_courses"][0]["id"] == "python"
    assert body["available_courses"][0]["selected"] is True

    persisted = client.get("/api/v1/my-learning")
    assert persisted.status_code == 200
    assert persisted.json()["active_course"]["id"] == "python"


def test_selecting_unknown_course_returns_404() -> None:
    client = TestClient(app)
    register_user(client)

    response = client.post("/api/v1/my-learning/courses", json={"course_id": "unknown"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found."
