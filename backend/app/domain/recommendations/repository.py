"""Recommendation database access."""

_current_recommendation: dict[str, str | None] = {
    "type": "start_exercise",
    "exercise_id": "ex_python_variables_1",
    "reason": "Start with Python variables because they are the first prerequisite.",
}

_initial_recommendation = _current_recommendation.copy()


def get_current_recommendation() -> dict[str, str | None]:
    return _current_recommendation.copy()


def set_current_recommendation(recommendation: dict[str, str | None]) -> None:
    _current_recommendation.clear()
    _current_recommendation.update(recommendation)


def reset_current_recommendation() -> None:
    _current_recommendation.clear()
    _current_recommendation.update(_initial_recommendation)
