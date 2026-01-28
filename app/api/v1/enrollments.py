from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.exceptions import DomainError
from app.schemas.enrollment import EnrollmentRequest
from app.services.enrollment_service import enroll_student
from app.core.database import get_db

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/")
def enroll_courses(
    request: EnrollmentRequest,
    db: Session = Depends(get_db)
):
    try:
        enroll_student(
            db=db,
            student_id=request.student_id,
            course_ids=request.course_ids
        )
        return {"status": "success"}
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))
