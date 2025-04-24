from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReactionBase(BaseModel):
    #id auto add by database
    review_id: int
    user_id: int
    is_liked: bool = False  # 預設為 False (未按讚)
    #reaction_time auto add by database

class ReactionCreate(ReactionBase):
    pass

class ReactionUpdate(ReactionBase):
    is_liked: Optional[bool] = None
    #reaction_time auto update by database

class Reaction(ReactionBase):
    id: int
    reaction_time: datetime

    class Config:
        orm_mode = True