from pydantic import BaseModel

class BuildingBase(BaseModel):
    lat: float
    lng: float
    name: str
    max_floor: int

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True
        populate_by_name = True  # 允許使用 field name（building_id）取代原始 alias（id）