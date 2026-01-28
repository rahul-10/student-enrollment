from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
