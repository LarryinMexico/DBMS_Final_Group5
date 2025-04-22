# app/models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    clerk_id = Column(String(128), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=True)
    email = Column(String(256), nullable=True)
    # role = Column(String(20), nullable=True)
    
    # 建立與Favorite的一對多關係
    favorites = relationship("Favorite", back_populates="user")

