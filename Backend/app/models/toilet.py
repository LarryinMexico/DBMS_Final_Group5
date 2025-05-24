# app/models/toilet.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.has import has 

class Toilet(Base):
    __tablename__ = "toilet"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    building_id = Column(Integer, ForeignKey("building.id"), nullable=False)
    floor = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)  # icon
    title = Column(String(20), nullable=False)
    
    # 建立與Building的多對一關係
    building = relationship("Building", back_populates="toilets")
    
    # 建立與Favorite的一對多關係
    favorites = relationship("Favorite", back_populates="toilet")

    # 建立與 Review 的一對多關係
    reviews = relationship("Review", back_populates="toilet")
    # 建立與 Amenity 的多對多關係
    amenities = relationship("Amenity", secondary=has, back_populates="toilets")
    # 建立與 Review 的一對多關係
    reports = relationship("Report", back_populates="toilet")
