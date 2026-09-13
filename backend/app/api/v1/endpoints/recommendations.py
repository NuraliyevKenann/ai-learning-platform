from fastapi import APIRouter

router = APIRouter()


@router.get("/current")
def get_current_recommendation() -> dict[str, str | None]:
    return {"recommendation": None}
