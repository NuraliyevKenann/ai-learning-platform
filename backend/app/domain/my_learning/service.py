"""My Learning application service."""

from app.domain.my_learning.repository import (
    get_course,
    list_courses,
    list_selected_course_records,
    select_course as select_course_in_repository,
)
from app.domain.my_learning.schemas import CourseListResponse, CourseSummary, MyLearningResponse


class CourseNotFoundError(Exception):
    """Raised when a requested course does not exist in the catalog."""


def list_available_courses(user_id: str) -> CourseListResponse:
    selected_by_course_id = _selected_record_map(user_id)
    return CourseListResponse(
        items=[_to_course_summary(course, selected_by_course_id) for course in list_courses()]
    )


def get_my_learning(user_id: str) -> MyLearningResponse:
    selected_by_course_id = _selected_record_map(user_id)
    available_courses = [
        _to_course_summary(course, selected_by_course_id)
        for course in list_courses()
    ]
    selected_courses = [course for course in available_courses if course.selected]
    return MyLearningResponse(
        selected_courses=selected_courses,
        active_course=selected_courses[0] if selected_courses else None,
        available_courses=available_courses,
    )


def select_course(user_id: str, course_id: str) -> MyLearningResponse:
    course = get_course(course_id)
    if course is None:
        raise CourseNotFoundError
    select_course_in_repository(user_id, str(course["id"]))
    return get_my_learning(user_id)


def _selected_record_map(user_id: str) -> dict[str, object]:
    return {
        record.course_id: record
        for record in list_selected_course_records(user_id)
    }


def _to_course_summary(course: dict, selected_by_course_id: dict[str, object]) -> CourseSummary:
    record = selected_by_course_id.get(str(course["id"]))
    return CourseSummary(
        **course,
        selected=record is not None,
        selected_at=getattr(record, "selected_at", None),
    )
