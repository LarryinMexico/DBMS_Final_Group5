# app/schemas/toilet.py
from pydantic import BaseModel
from typing import Optional

class ToiletBase(BaseModel):
    building_id: int
    floor: int
    type: str
    title: str

class ToiletCreate(ToiletBase):
    pass

class ToiletUpdate(BaseModel):
    building_id: Optional[int] = None
    floor: Optional[int] = None
    type: Optional[str] = None
    title: Optional[str] = None

class ToiletOut(ToiletBase):
    id: int

    model_config = {"from_attributes": True}