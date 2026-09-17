"""My Learning endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.domain.my_learning.schemas import CourseListResponse, MyLearningResponse, SelectCourseRequest
from app.domain.my_learning.service import (
    CourseNotFoundError,
    get_my_learning as get_my_learning_from_service,
    list_available_courses,
    select_course as select_course_from_service,
)
from app.domain.users.models import User

router = APIRouter()


@router.get("", response_model=MyLearningResponse)
def read_my_learning(user: User = Depends(get_current_user)) -> MyLearningResponse:
    return get_my_learning_from_service(user.id)


@router.get("/courses", response_model=CourseListResponse)
def list_courses(user: User = Depends(get_current_user)) -> CourseListResponse:
    return list_available_courses(user.id)


@router.post("/courses", response_model=MyLearningResponse)
def select_course(
    payload: SelectCourseRequest,
    user: User = Depends(get_current_user),
) -> MyLearningResponse:
    try:
        return select_course_from_service(user.id, payload.course_id)
    except CourseNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Course not found.") from exc
