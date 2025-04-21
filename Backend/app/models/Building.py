# app/models/toilet.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Building(Base):
    __tablename__ = "building"
    building_id = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Integer, nullable=False)
    lng = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False)
    max_floor = Column(Integer, nullable=False)
