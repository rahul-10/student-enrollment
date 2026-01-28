from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base

class StudentCourse(Base):
    __tablename__ = "student_courses"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
