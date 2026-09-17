from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    attempts,
    dashboard,
    exercises,
    goals,
    knowledge,
    my_learning,
    recommendations,
    topics,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(attempts.router, prefix="/attempts", tags=["attempts"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(my_learning.router, prefix="/my-learning", tags=["my-learning"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
