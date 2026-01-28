from sqlalchemy import Column, Integer, String, Time, ForeignKey
from app.models.base import Base

class CourseTimetable(Base):
    __tablename__ = "course_timetables"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    day_of_week = Column(String(10), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
