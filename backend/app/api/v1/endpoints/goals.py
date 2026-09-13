from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_goals() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
