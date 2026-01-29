from pydantic import BaseModel
from datetime import time


class TimetableCreateRequest(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time


class TimetableUpdateRequest(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time
