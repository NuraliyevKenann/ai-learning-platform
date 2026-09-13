from fastapi import APIRouter

from app.api.v1.endpoints import attempts, exercises, goals, knowledge, recommendations, topics

api_router = APIRouter()

api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(attempts.router, prefix="/attempts", tags=["attempts"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(
    recommendations.router, prefix="/recommendations", tags=["recommendations"]
)


@api_router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
