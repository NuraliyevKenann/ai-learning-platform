"""Content request/response schemas."""

from pydantic import BaseModel


class Goal(BaseModel):
    id: str
    title: str
    description: str


class Topic(BaseModel):
    id: str
    goal_id: str
    title: str
    skill_id: str
    order: int


class Exercise(BaseModel):
    id: str
    topic_id: str
    skill_id: str
    title: str
    prompt: str
    difficulty: str
    estimated_minutes: int
    hint: str


class GoalListResponse(BaseModel):
    items: list[Goal]


class TopicListResponse(BaseModel):
    items: list[Topic]


class ExerciseListResponse(BaseModel):
    items: list[Exercise]
