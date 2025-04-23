from pydantic import BaseModel

class ReviewBase(BaseModel):
    user_id: int
    toilet_id: int
    rating: int

class ReviewCreate(ReviewBase):
    pass

class ReviewOut(ReviewBase):
    id: int
    class Config:
        orm_mode = True