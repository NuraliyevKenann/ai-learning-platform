from app.learning_engine.mastery import update_mastery


def test_update_mastery_blends_old_mastery_with_attempt_score() -> None:
    assert update_mastery(old_mastery=50, attempt_score=100) == 65
