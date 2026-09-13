from fastapi import APIRouter

router = APIRouter()


@router.post("")
def submit_attempt() -> dict[str, str]:
    return {"status": "not_implemented"}
