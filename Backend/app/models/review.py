from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):
    __tablename__ = "review"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    toilet_id = Column(Integer, ForeignKey("toilet.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(255), nullable=True)
    createAt = Column(DateTime, default=func.now(), nullable=False)
    updateAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


    # 建立與User的多對一關係
    user = relationship("User", back_populates="reviews")
    
    # 建立與Toilet的多對一關係
    toilet = relationship("Toilet", back_populates="reviews")

    # 建立與reaction的多對一關係
    reactions = relationship("Reaction", back_populates="review") 

