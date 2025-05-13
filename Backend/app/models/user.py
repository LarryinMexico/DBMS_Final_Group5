# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String(128), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=True)
    email = Column(String(256), nullable=True)
    avatarUrl = Column(String(512), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    # role = Column(String(20), nullable=True)
    
    # 建立與Favorite的一對多關係
    favorites = relationship("Favorite", back_populates="user")

    # 建立與Review的一對多關係
    reviews = relationship("Review", back_populates="user")

    # 建立與 Reaction 的一對多關係
    reactions = relationship("Reaction", back_populates="user") 

    # 追蹤別人的關係（我追蹤了誰）
    following_relations = relationship(
        "Follow",
        foreign_keys="[Follow.following_id]",
        back_populates="following",
    )

    # 被追蹤的關係（誰追蹤我）
    followed_relations = relationship(
        "Follow",
        foreign_keys="[Follow.followed_id]",
        back_populates="followed",
    )