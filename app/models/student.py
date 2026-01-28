from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
