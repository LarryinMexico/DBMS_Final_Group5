# app/models/has.py
from sqlalchemy import Column, Integer, ForeignKey, Table
from app.db.base import Base

# 多對多的中間表
class Has(Base):
    __tablename__ = "has"
    
    toilet_id = Column(Integer, ForeignKey("toilet.id"), primary_key=True)
    amenity_id = Column(Integer, ForeignKey("amenities.id"), primary_key=True)