from pydantic import BaseModel, Field
from typing import Optional

class Search(BaseModel):
    max_floor: Optional[int] = Field(None, description="可接受的最高樓層")
    min_review_count: Optional[int] = Field(None, description="最少評論數")
    min_average_rating: Optional[float] = Field(None, description="最低平均評分")
    amenity_id: Optional[int] = Field(None, description="所需的 amenity ID")

    model_config = {"from_attributes": True}
