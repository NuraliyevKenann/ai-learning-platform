"""Recommendation database access."""

_initial_recommendation: dict[str, str | None] = {
    "type": "start_exercise",
    "exercise_id": "ex_python_variables_1",
    "reason": "Start with Python variables because they are the first prerequisite.",
}
_recommendation_by_user: dict[str, dict[str, str | None]] = {}


def _get_or_create_recommendation(user_id: str) -> dict[str, str | None]:
    return _recommendation_by_user.setdefault(user_id, _initial_recommendation.copy())


def get_current_recommendation(user_id: str) -> dict[str, str | None]:
    return _get_or_create_recommendation(user_id).copy()


def set_current_recommendation(user_id: str, recommendation: dict[str, str | None]) -> None:
    _recommendation_by_user[user_id] = recommendation.copy()


def reset_current_recommendation(user_id: str) -> None:
    _recommendation_by_user[user_id] = _initial_recommendation.copy()


def clear_all_recommendations_for_tests() -> None:
    _recommendation_by_user.clear()
