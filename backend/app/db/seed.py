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
    {
        "id": "topic_python_functions",
        "goal_id": "goal_python_backend",
        "title": "Python functions",
        "skill_id": "skill_python_functions",
        "order": 3,
    },
    {
        "id": "topic_python_lists",
        "goal_id": "goal_python_backend",
        "title": "Python lists",
        "skill_id": "skill_python_lists",
        "order": 4,
    },
    {
        "id": "topic_python_dicts",
        "goal_id": "goal_python_backend",
        "title": "Python dictionaries",
        "skill_id": "skill_python_dicts",
        "order": 5,
    },
    {
        "id": "topic_fastapi_path_params",
        "goal_id": "goal_python_backend",
        "title": "FastAPI path parameters",
        "skill_id": "skill_fastapi_path_params",
        "order": 6,
    },
    {
        "id": "topic_fastapi_request_body",
        "goal_id": "goal_python_backend",
        "title": "FastAPI request body",
        "skill_id": "skill_fastapi_request_body",
        "order": 7,
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
        "order": 1,
    },
    {
        "id": "ex_fastapi_health_1",
        "topic_id": "topic_fastapi_health",
        "skill_id": "skill_fastapi_routes",
        "prompt": "What JSON should the health endpoint return when the backend is OK?",
        "expected_answer": '{"status": "ok"}',
        "difficulty": "easy",
        "order": 2,
    },
    {
        "id": "ex_python_functions_1",
        "topic_id": "topic_python_functions",
        "skill_id": "skill_python_functions",
        "prompt": "Create a function named greet that returns the text hello.",
        "expected_answer": "def greet():\n    return \"hello\"",
        "difficulty": "easy",
        "order": 3,
    },
    {
        "id": "ex_python_lists_1",
        "topic_id": "topic_python_lists",
        "skill_id": "skill_python_lists",
        "prompt": "Create a list named numbers containing 1, 2, and 3.",
        "expected_answer": "numbers = [1, 2, 3]",
        "difficulty": "easy",
        "order": 4,
    },
    {
        "id": "ex_python_dicts_1",
        "topic_id": "topic_python_dicts",
        "skill_id": "skill_python_dicts",
        "prompt": "Create a dictionary named user with name set to Ali.",
        "expected_answer": "user = {\"name\": \"Ali\"}",
        "difficulty": "easy",
        "order": 5,
    },
    {
        "id": "ex_fastapi_path_params_1",
        "topic_id": "topic_fastapi_path_params",
        "skill_id": "skill_fastapi_path_params",
        "prompt": "What path should be used for an endpoint that receives an item_id path parameter?",
        "expected_answer": "/items/{item_id}",
        "difficulty": "medium",
        "order": 6,
    },
    {
        "id": "ex_fastapi_request_body_1",
        "topic_id": "topic_fastapi_request_body",
        "skill_id": "skill_fastapi_request_body",
        "prompt": "What JSON request body creates a user named Ali?",
        "expected_answer": '{"name": "Ali"}',
        "difficulty": "medium",
        "order": 7,
    },
]
