# app/schemas/favorite.py

from pydantic import BaseModel

class FavoriteCheck(BaseModel):
    UserID: int

class FavoriteAdd(BaseModel):
    UserID: int
    ToiletID: int

class FavoriteDel(BaseModel):
    FavoriteID: int