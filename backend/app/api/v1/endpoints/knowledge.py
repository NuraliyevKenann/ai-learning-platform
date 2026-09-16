from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.learning.schemas import KnowledgeStateResponse, ResetKnowledgeStateResponse
from app.domain.learning.service import get_knowledge_state as get_knowledge_state_from_service
from app.domain.learning.service import reset_knowledge_state as reset_knowledge_state_from_service
from app.domain.users.models import User

router = APIRouter()


@router.get("/state", response_model=KnowledgeStateResponse)
def get_knowledge_state(user: User = Depends(get_current_user)) -> KnowledgeStateResponse:
    return KnowledgeStateResponse(items=get_knowledge_state_from_service(user.id))


@router.post("/reset", response_model=ResetKnowledgeStateResponse)
def reset_knowledge_state(user: User = Depends(get_current_user)) -> ResetKnowledgeStateResponse:
    return reset_knowledge_state_from_service(user.id)
