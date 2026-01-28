from sqlalchemy.orm import Session
from app.repositories import student_repo, course_repo, enrollment_repo

from app.core.exceptions import (
    StudentNotFoundError,
    CourseNotFoundError,
    TimetableClashError, CourseListEmptyError,
)

def enroll_student(db, student_id: int, course_ids: list[int]):

    student = student_repo.get_student_by_id(db, student_id)
    if not student:
        raise StudentNotFoundError(f"Student {student_id} not found")

    if not course_ids:
        raise CourseListEmptyError(f"Course list can not be empty")
    courses = course_repo.get_courses_by_ids_and_college_id(db, course_ids, student_id)
    if len(courses) != len(course_ids):
        raise CourseNotFoundError("One or more courses do not belong to the student's college")

    if enrollment_repo.has_timetable_clash(db, student_id, course_ids):
        raise TimetableClashError("Timetable clash detected")

    enrollment_repo.create_enrollments(db, student_id, course_ids)
