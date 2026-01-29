from sqlalchemy.orm import Session
from app.core.exceptions import CourseNotFoundError, TimetableClashError
from app.models import CourseTimetable
from app.repositories import course_repo, timetable_repo

def add_course_timetable(
    db: Session,
    course_id: int,
    day_of_week: str,
    start_time,
    end_time
):
    course = course_repo.get_course_by_id(db, course_id)
    if not course:
        raise CourseNotFoundError("Course not found")

    if timetable_repo.causes_clash_for_enrolled_students(
        db, course_id, day_of_week, start_time, end_time
    ):
        raise TimetableClashError(
            "Timetable change causes clash for enrolled students"
        )

    timetable = CourseTimetable(
        course_id=course_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time
    )

    return timetable_repo.create_timetable(db, timetable)


def update_course_timetable(
    db: Session,
    timetable_id: int,
    day_of_week: str,
    start_time,
    end_time
):
    timetable = timetable_repo.get_timetable_by_id(db, timetable_id)
    if not timetable:
        raise ValueError("Timetable not found")

    if timetable_repo.causes_clash_for_enrolled_students(
        db,
        timetable.course_id,
        day_of_week,
        start_time,
        end_time,
        exclude_timetable_id=timetable.id
    ):
        raise TimetableClashError(
            "Timetable update causes clash for enrolled students"
        )

    timetable.day_of_week = day_of_week
    timetable.start_time = start_time
    timetable.end_time = end_time

    db.commit()
    return timetable

def delete_course_timetable(db: Session, timetable_id: int):
    timetable = timetable_repo.get_timetable_by_id(db, timetable_id)
    if not timetable:
        raise ValueError("Timetable not found")

    timetable_repo.delete_timetable(db, timetable)


