# app/models/toilet.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Toilet(Base):
    __tablename__ = "toilet"
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False) # icon
    title = Column(String(20), nullable=False)