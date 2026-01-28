from sqlalchemy.orm import Session
from app.models.course import Course


def get_courses_by_ids_and_college_id(
    db: Session,
    course_ids: list[int],
    college_id: int
) -> list[Course]:
    """
    Fetch courses by IDs that belong to a specific college.
    """
    if not course_ids:
        return []

    return (
        db.query(Course)
        .filter(
            Course.id.in_(course_ids),
            Course.college_id == college_id
        )
        .all()
    )
