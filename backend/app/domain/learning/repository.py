"""Learning database access."""

USER_ID = "demo_user"

_knowledge_state: dict[str, float] = {
    "skill_python_variables": 0.0,
    "skill_fastapi_routes": 0.0,
}

_initial_knowledge_state = _knowledge_state.copy()


def get_user_id() -> str:
    return USER_ID


def list_skill_mastery() -> dict[str, float]:
    return _knowledge_state.copy()


def get_mastery(skill_id: str) -> float:
    return _knowledge_state.get(skill_id, 0.0)


def set_mastery(skill_id: str, mastery: float) -> None:
    _knowledge_state[skill_id] = mastery


def reset_knowledge_state() -> None:
    _knowledge_state.clear()
    _knowledge_state.update(_initial_knowledge_state)
