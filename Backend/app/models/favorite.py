from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorite"

    FavoriteID = Column(Integer,primary_key=True,index=True)
    UserID = Column(Integer,nullable=False)
    ToiletID = Column(Integer,nullable=False)

