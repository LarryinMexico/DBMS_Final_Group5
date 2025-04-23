# app/schemas/favorite.py

from pydantic import BaseModel

class FavoriteCheck(BaseModel):
    user_id: int

class FavoriteAdd(BaseModel):
    user_id: int
    toilet_id: int

class FavoriteDel(BaseModel):
    user_id: int
    toilet_id: int