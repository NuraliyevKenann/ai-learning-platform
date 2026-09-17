"""Dashboard summary orchestration."""

from app.domain.assessment.repository import list_attempt_history
from app.domain.content.repository import get_exercise_by_id, list_exercises, list_goals
from app.domain.content.schemas import Exercise, Goal
from app.domain.dashboard.schemas import DashboardSummaryResponse
from app.domain.learning.service import get_knowledge_state
from app.domain.recommendations.service import get_current_recommendation
from app.domain.users.models import User
from app.domain.users.service import to_user_response


def get_dashboard_summary(user: User, recent_attempt_limit: int = 4) -> DashboardSummaryResponse:
    knowledge = get_knowledge_state(user.id)
    attempts = list_attempt_history(user.id)
    recent_attempts = attempts[:recent_attempt_limit]
    recommendation = get_current_recommendation(user.id)
    goals = list_goals()
    exercises = list_exercises()
    current_exercise = _find_current_exercise(recommendation.exercise_id, exercises)

    total_skills = len(knowledge)
    completed_skills = sum(1 for item in knowledge if item.mastery >= 70)
    average_mastery = (
        round(sum(item.mastery for item in knowledge) / total_skills)
        if total_skills
        else 0
    )

    return DashboardSummaryResponse(
        user=to_user_response(user),
        goal=Goal(**goals[0]) if goals else None,
        current_exercise=current_exercise,
        current_recommendation=recommendation,
        knowledge=knowledge,
        recent_attempts=recent_attempts,
        average_mastery=average_mastery,
        completed_skills=completed_skills,
        total_skills=total_skills,
        total_attempts=len(attempts),
        correct_attempts=sum(1 for attempt in attempts if attempt.is_correct),
    )


def _find_current_exercise(exercise_id: str | None, exercises: list[dict]) -> Exercise | None:
    selected_exercise = get_exercise_by_id(exercise_id) if exercise_id else None
    if selected_exercise is None:
        selected_exercise = exercises[0] if exercises else None
    if selected_exercise is None:
        return None
    return Exercise(**{key: value for key, value in selected_exercise.items() if key != "expected_answer"})
