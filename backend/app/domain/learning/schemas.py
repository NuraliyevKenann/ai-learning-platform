"""Learning request/response schemas."""

from pydantic import BaseModel


class KnowledgeStateItem(BaseModel):
    user_id: str
    skill_id: str
    mastery: float
    level: str


class KnowledgeStateResponse(BaseModel):
    items: list[KnowledgeStateItem]


class ResetKnowledgeStateResponse(BaseModel):
    status: str
    items: list[KnowledgeStateItem]
