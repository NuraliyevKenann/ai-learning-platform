"""Seed data for the first Python Backend Developer learning path."""

GOALS = [
    {
        "id": "goal_python_backend",
        "title": "Python Backend Developer",
        "description": "Build a small FastAPI backend and understand the learning loop.",
    }
]

TOPICS = [
    {
        "id": "topic_python_variables",
        "goal_id": "goal_python_backend",
        "title": "Python variables",
        "skill_id": "skill_python_variables",
        "order": 1,
    },
    {
        "id": "topic_fastapi_health",
        "goal_id": "goal_python_backend",
        "title": "FastAPI health endpoint",
        "skill_id": "skill_fastapi_routes",
        "order": 2,
    },
]

EXERCISES = [
    {
        "id": "ex_python_variables_1",
        "topic_id": "topic_python_variables",
        "skill_id": "skill_python_variables",
        "prompt": "Create a variable named x with the value 5.",
        "expected_answer": "x = 5",
        "difficulty": "easy",
    },
    {
        "id": "ex_fastapi_health_1",
        "topic_id": "topic_fastapi_health",
        "skill_id": "skill_fastapi_routes",
        "prompt": "What JSON should the health endpoint return when the backend is OK?",
        "expected_answer": '{"status": "ok"}',
        "difficulty": "easy",
    },
]
