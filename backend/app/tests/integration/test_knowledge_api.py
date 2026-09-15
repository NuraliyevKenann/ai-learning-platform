from fastapi.testclient import TestClient

from app.domain.learning.repository import reset_knowledge_state
from app.domain.recommendations.repository import reset_current_recommendation
from app.main import app


def test_reset_knowledge_state_returns_mastery_to_zero() -> None:
    reset_knowledge_state()
    reset_current_recommendation()

    client = TestClient(app)

    client.post(
        "/api/v1/attempts",
        json={
            "exercise_id": "ex_python_variables_1",
            "answer": "x = 5",
        },
    )

    response = client.post("/api/v1/knowledge/reset")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "items": [
            {
                "user_id": "demo_user",
                "skill_id": "skill_python_variables",
                "mastery": 0.0,
                "level": "weak",
            },
            {
                "user_id": "demo_user",
                "skill_id": "skill_fastapi_routes",
                "mastery": 0.0,
                "level": "weak",
            },
        ],
    }
