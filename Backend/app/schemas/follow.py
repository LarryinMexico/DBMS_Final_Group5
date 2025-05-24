from pydantic import BaseModel
from datetime import datetime

class FollowCreate(BaseModel):
    #id auto add by database
    following_id: int
    followed_id: int
    #follow_at auto add by database

class FollowOut(FollowCreate):
    id: int
    follow_at: datetime
    class Config:
        orm_mode = True