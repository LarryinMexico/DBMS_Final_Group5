from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Follow(Base):
    __tablename__ = "follow"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #追蹤別人的人
    following_id = Column(Integer, ForeignKey("users.id"))
    #被追蹤的人
    followed_id = Column(Integer, ForeignKey("users.id"))
    follow_at = Column(DateTime, default=func.now(), onupdate=func.now())

     # 跟 user 建立關聯（追蹤別人的人）
    following = relationship("User", foreign_keys=[following_id], back_populates="following_relations")

    # 跟 user 建立關聯（被追蹤的人）
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followed_relations")
