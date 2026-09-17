"""My Learning API schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class CourseSummary(BaseModel):
    id: str
    title: str
    description: str
    status: str
    goal_id: str | None = None
    selected: bool = False
    selected_at: datetime | None = None


class CourseListResponse(BaseModel):
    items: list[CourseSummary]


class SelectCourseRequest(BaseModel):
    course_id: str = Field(min_length=2, max_length=80)


class MyLearningResponse(BaseModel):
    selected_courses: list[CourseSummary]
    active_course: CourseSummary | None
    available_courses: list[CourseSummary]
