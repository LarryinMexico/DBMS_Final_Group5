from pydantic import BaseModel
from typing import Optional

class ReviewBase(BaseModel):
    user_id: int
    toilet_id: int
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    user_id: Optional[int] = None
    toilet_id: Optional[int] = None
    rating: Optional[int] = None

class ReviewOut(ReviewBase):
    review_id: int
    class Config:
        orm_mode = True