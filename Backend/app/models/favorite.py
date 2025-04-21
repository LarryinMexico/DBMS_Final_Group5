from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,nullable=False)
    toilet_id = Column(Integer,nullable=False)

