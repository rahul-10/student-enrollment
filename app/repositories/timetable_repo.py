from sqlalchemy.orm import Session, aliased
from app.models import CourseTimetable, StudentCourse
from typing import Optional


def get_timetable_by_id(db: Session, timetable_id: int):
    return (
        db.query(CourseTimetable)
        .filter(CourseTimetable.id == timetable_id)
        .one_or_none()
    )


def create_timetable(db: Session, timetable: CourseTimetable):
    db.add(timetable)
    db.commit()
    db.refresh(timetable)
    return timetable


def delete_timetable(db: Session, timetable: CourseTimetable):
    db.delete(timetable)
    db.commit()

def causes_clash_for_enrolled_students(
    db: Session,
    course_id: int,
    day_of_week: str,
    start_time,
    end_time,
    exclude_timetable_id: Optional[int] = None
) -> bool:
    ct_existing = aliased(CourseTimetable)

    query = (
        db.query(StudentCourse)
        .join(ct_existing, StudentCourse.course_id == ct_existing.course_id)
        .filter(
            StudentCourse.course_id == course_id,
            ct_existing.day_of_week == day_of_week,
            ct_existing.start_time < end_time,
            start_time < ct_existing.end_time
        )
    )

    if exclude_timetable_id is not None:
        query = query.filter(ct_existing.id != exclude_timetable_id)

    return db.query(query.exists()).scalar()
