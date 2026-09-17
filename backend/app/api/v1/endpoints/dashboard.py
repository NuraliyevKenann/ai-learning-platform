from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domain.dashboard.schemas import DashboardSummaryResponse
from app.domain.dashboard.service import get_dashboard_summary
from app.domain.users.models import User

router = APIRouter()


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_summary(user: User = Depends(get_current_user)) -> DashboardSummaryResponse:
    return get_dashboard_summary(user)
