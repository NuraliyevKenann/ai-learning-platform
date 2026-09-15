from fastapi import APIRouter

from app.domain.content.schemas import TopicListResponse
from app.domain.content.service import list_topics as list_topics_from_service

router = APIRouter()


@router.get("", response_model=TopicListResponse)
def list_topics() -> TopicListResponse:
    return TopicListResponse(items=list_topics_from_service())
