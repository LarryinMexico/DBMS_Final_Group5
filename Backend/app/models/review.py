from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    toilet_id = Column(Integer, ForeignKey("toilet.id"), nullable=False)
    rating = Column(Integer, nullable=False)

    # 建立與User的多對一關係
    user = relationship("User", back_populates="reviews")
    
    # 建立與Toilet的多對一關係
    toilet = relationship("Toilet", back_populates="reviews")

