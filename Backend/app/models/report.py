from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Report(Base):
    __tablename__ = "report"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    toilet_id = Column(Integer, ForeignKey("toilet.id"), nullable=False)
    IssueDescription = Column(String(255), nullable=False)

    # 建立與User的多對一關係
    user = relationship("User", back_populates="reports")

    # 建立與User的多對一關係
    toilet = relationship("Toilet", back_populates="reports")

