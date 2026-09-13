from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_topics() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
