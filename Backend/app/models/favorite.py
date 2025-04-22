from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorite"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    toilet_id = Column(Integer, ForeignKey("toilet.id"), nullable=False)
    
    # 建立與User的多對一關係
    user = relationship("User", back_populates="favorites")
    
    # 建立與Toilet的多對一關係
    toilet = relationship("Toilet", back_populates="favorites")

