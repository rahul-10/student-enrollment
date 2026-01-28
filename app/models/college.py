from sqlalchemy import Column, Integer, String
from app.models.base import Base

class College(Base):
    __tablename__ = "colleges"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
