import { apiGet, apiPost } from "./client";
import type { MyLearningResponse, CourseListResponse } from "../types/domain";

export function getMyLearning() {
  return apiGet<MyLearningResponse>("/my-learning");
}

export function getMyLearningCourses() {
  return apiGet<CourseListResponse>("/my-learning/courses");
}

export function selectMyLearningCourse(courseId: string) {
  return apiPost<MyLearningResponse>("/my-learning/courses", { course_id: courseId });
}
