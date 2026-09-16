"""Knowledge state updates and progress logic."""

from app.domain.learning.repository import list_skill_mastery
from app.domain.learning.repository import reset_knowledge_state as reset_knowledge_state_in_repository
from app.domain.learning.schemas import KnowledgeStateItem, ResetKnowledgeStateResponse
from app.domain.recommendations.repository import reset_current_recommendation
from app.learning_engine.rules import classify_mastery


def get_knowledge_state(user_id: str) -> list[KnowledgeStateItem]:
    return [
        KnowledgeStateItem(
            user_id=user_id,
            skill_id=skill_id,
            mastery=mastery,
            level=classify_mastery(mastery),
        )
        for skill_id, mastery in list_skill_mastery(user_id).items()
    ]


def reset_knowledge_state(user_id: str) -> ResetKnowledgeStateResponse:
    reset_knowledge_state_in_repository(user_id)
    reset_current_recommendation(user_id)
    return ResetKnowledgeStateResponse(
        status="ok",
        items=get_knowledge_state(user_id),
    )
