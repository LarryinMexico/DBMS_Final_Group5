from pydantic import BaseModel

class BuildingBase(BaseModel):
    lat: int
    lng: int
    name: str
    max_floor: int

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    building_id: int

    class Config:
        from_attributes = True 