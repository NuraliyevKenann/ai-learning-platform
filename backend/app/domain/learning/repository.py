"""Learning database access."""

_initial_knowledge_state: dict[str, float] = {
    "skill_python_variables": 0.0,
    "skill_fastapi_routes": 0.0,
}
_knowledge_state_by_user: dict[str, dict[str, float]] = {}


def _get_or_create_state(user_id: str) -> dict[str, float]:
    return _knowledge_state_by_user.setdefault(user_id, _initial_knowledge_state.copy())


def list_skill_mastery(user_id: str) -> dict[str, float]:
    return _get_or_create_state(user_id).copy()


def get_mastery(user_id: str, skill_id: str) -> float:
    return _get_or_create_state(user_id).get(skill_id, 0.0)


def set_mastery(user_id: str, skill_id: str, mastery: float) -> None:
    _get_or_create_state(user_id)[skill_id] = mastery


def reset_knowledge_state(user_id: str) -> None:
    _knowledge_state_by_user[user_id] = _initial_knowledge_state.copy()


def clear_all_knowledge_for_tests() -> None:
    _knowledge_state_by_user.clear()
