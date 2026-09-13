from fastapi import APIRouter

router = APIRouter()


@router.get("/state")
def get_knowledge_state() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
