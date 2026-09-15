"""Knowledge state updates and progress logic."""

from app.domain.learning.repository import (
    get_user_id,
    list_skill_mastery,
    reset_knowledge_state as reset_knowledge_state_in_repository,
)
from app.domain.learning.schemas import KnowledgeStateItem, ResetKnowledgeStateResponse
from app.domain.recommendations.repository import reset_current_recommendation
from app.learning_engine.rules import classify_mastery


def get_knowledge_state() -> list[KnowledgeStateItem]:
    return [
        KnowledgeStateItem(
            user_id=get_user_id(),
            skill_id=skill_id,
            mastery=mastery,
            level=classify_mastery(mastery),
        )
        for skill_id, mastery in list_skill_mastery().items()
    ]


def reset_knowledge_state() -> ResetKnowledgeStateResponse:
    reset_knowledge_state_in_repository()
    reset_current_recommendation()
    return ResetKnowledgeStateResponse(
        status="ok",
        items=get_knowledge_state(),
    )
