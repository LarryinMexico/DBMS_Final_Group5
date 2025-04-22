from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from app.db.base import Base

class Building(Base):
    __tablename__ = "building"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    lat = Column(DECIMAL(9, 6), nullable=False)  # 可儲存 ±999.999999
    lng = Column(DECIMAL(9, 6), nullable=False)
    name = Column(String(20), nullable=False)
    max_floor = Column(Integer, nullable=False)
    
    # 建立與Toilet的一對多關係
    toilets = relationship("Toilet", back_populates="building")
