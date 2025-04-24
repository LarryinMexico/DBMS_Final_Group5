from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    #id: Optional[int] = None #auto add by database
    user_id: int
    toilet_id: int
    rating: int
    comment: Optional[str] = None
    createAt: Optional[datetime] = None #auto add by database
    updateAt: Optional[datetime] = None #auto add by database

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    user_id: Optional[int] = None
    toilet_id: Optional[int] = None
    rating: Optional[int] = None
    comment: Optional[str] = None
    updateAt: Optional[datetime] = None
    

class ReviewOut(ReviewBase):
    id: int
    createAt: datetime
    updateAt: datetime
    class Config:
        orm_mode = True