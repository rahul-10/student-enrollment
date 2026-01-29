from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.admin_timetable import (
    TimetableCreateRequest,
    TimetableUpdateRequest
)
from app.services.admin_timetable_service import (
    add_course_timetable,
    update_course_timetable,
    delete_course_timetable
)
from app.core.exceptions import DomainError

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/courses/{course_id}/timetable")
def create_timetable(
    course_id: int,
    request: TimetableCreateRequest,
    db: Session = Depends(get_db)
):
    try:
        return add_course_timetable(
            db,
            course_id,
            request.day_of_week,
            request.start_time,
            request.end_time
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/timetables/{timetable_id}")
def update_timetable(
    timetable_id: int,
    request: TimetableUpdateRequest,
    db: Session = Depends(get_db)
):
    try:
        return update_course_timetable(
            db,
            timetable_id,
            request.day_of_week,
            request.start_time,
            request.end_time
        )
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/timetables/{timetable_id}")
def remove_timetable(
    timetable_id: int,
    db: Session = Depends(get_db)
):
    delete_course_timetable(db, timetable_id)
    return {"status": "deleted"}
