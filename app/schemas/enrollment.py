from pydantic import BaseModel
from typing import List

class EnrollmentRequest(BaseModel):
    student_id: int # This should be consumed from token in prod env
    course_ids: List[int]
