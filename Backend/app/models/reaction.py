from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Reaction(Base):
    __tablename__ = "reaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_id = Column(Integer, ForeignKey("review.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_liked = Column(Boolean, default=False)
    #reaction time will update everytime the user change the is_liked status
    reaction_time = Column(DateTime, default=func.now(), onupdate=func.now())

    review = relationship("Review", back_populates="reactions")
    user = relationship("User", back_populates="reactions")
