from sqlalchemy.orm import Session,  aliased
from app.models import CourseTimetable, StudentCourse

def check_timetable_clash(db: Session, student_id: int, course_ids: list[int]):
    clash_exists = db.query(StudentCourse).join(
        CourseTimetable,
        StudentCourse.course_id == CourseTimetable.course_id
    ).filter(
        StudentCourse.student_id == student_id,
        CourseTimetable.course_id.in_(course_ids)
    ).first()

    if clash_exists:
        raise ValueError("Timetable clash detected")

def create_enrollments(db: Session, student_id: int, course_ids: list[int]):
    enrollments = [
        StudentCourse(student_id=student_id, course_id=cid)
        for cid in course_ids
    ]
    db.add_all(enrollments)
    db.commit()


def has_timetable_clash(
    db: Session,
    student_id: int,
    course_ids: list[int]
) -> bool:
    """
    Returns True if enrolling the given courses would cause a timetable clash
    for the student.
    """
    if not course_ids:
        return False

    ct_existing = aliased(CourseTimetable)
    ct_new = aliased(CourseTimetable)

    return (
        db.query(StudentCourse)
        .join(
            ct_existing,
            StudentCourse.course_id == ct_existing.course_id
        )
        .join(
            ct_new,
            ct_new.course_id.in_(course_ids)
        )
        .filter(
            StudentCourse.student_id == student_id,
            ct_existing.day_of_week == ct_new.day_of_week,
            ct_existing.start_time < ct_new.end_time,
            ct_new.start_time < ct_existing.end_time,
        )
        .first()
        is not None
    )