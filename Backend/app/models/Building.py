# app/models/toilet.py
from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Building(Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    name = Column(String(20), nullable=False)
    max_floor = Column(Integer, nullable=False)
