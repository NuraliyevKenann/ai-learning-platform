from fastapi import APIRouter

from app.domain.learning.schemas import KnowledgeStateResponse, ResetKnowledgeStateResponse
from app.domain.learning.service import get_knowledge_state as get_knowledge_state_from_service
from app.domain.learning.service import reset_knowledge_state as reset_knowledge_state_from_service

router = APIRouter()


@router.get("/state", response_model=KnowledgeStateResponse)
def get_knowledge_state() -> KnowledgeStateResponse:
    return KnowledgeStateResponse(items=get_knowledge_state_from_service())


@router.post("/reset", response_model=ResetKnowledgeStateResponse)
def reset_knowledge_state() -> ResetKnowledgeStateResponse:
    return reset_knowledge_state_from_service()
