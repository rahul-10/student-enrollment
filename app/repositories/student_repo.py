from sqlalchemy.orm import Session
from app.models.student import Student


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    """
    Fetch a student by ID.
    """
    return (
        db.query(Student)
        .filter(Student.id == student_id)
        .one_or_none()
    )
