def update_mastery(old_mastery: float, attempt_score: float, weight: float = 0.3) -> float:
    """Blend old mastery with a new attempt score.

    Values are represented from 0 to 100. This simple rule is intentionally
    understandable and testable before any ML is introduced.
    """
    bounded_old = max(0.0, min(100.0, old_mastery))
    bounded_score = max(0.0, min(100.0, attempt_score))
    bounded_weight = max(0.0, min(1.0, weight))
    return round((bounded_old * (1 - bounded_weight)) + (bounded_score * bounded_weight), 2)
