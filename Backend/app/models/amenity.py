from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from app.db.base import Base

class Amenity(Base):
    __tablename__ = "amenity"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(20), nullable=False)
    
    # 建立與Toilet的一對多關係
    toilets = relationship(
            "Toilet",
            secondary="has",
            back_populates="amenities"
        )