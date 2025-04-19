# app/schemas/favorite.py

from pydantic import BaseModel

class FavoriteCheck():
    UserID: int

class FavoriteAdd():
    UserID: int
    ToiletID: int

class FavoriteDel():
    FavoriteID: int