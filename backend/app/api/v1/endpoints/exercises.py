from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_exercises() -> dict[str, list[dict[str, str]]]:
    return {"items": []}
