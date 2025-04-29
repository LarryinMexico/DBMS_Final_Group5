from pydantic import BaseModel
from typing import List

class AmenityBase(BaseModel):
    name: str

class AmenityCreate(AmenityBase):
    pass

class Amenity(AmenityBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True 

class ToiletWithAmenities(BaseModel):
    id: int
    name: str

    amenities: List[Amenity] = []
    class Config:
        from_attributes = True