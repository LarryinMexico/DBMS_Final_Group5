from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.CRUD import favorite as crud_favorite
from app.schemas import favorite as favorite_schema
from app.db.session import get_db
from typing import List

router = APIRouter()

@router.post("/getList")
def list_favorite(
    user: favorite_schema.FavoriteCheck,
    db: Session = Depends(get_db)
):
    return crud_favorite.get_favorite_list(db, user.user_id)

@router.post("/addList")
def add_favorite(
    user: favorite_schema.FavoriteAdd,
    db: Session = Depends(get_db)
):
    if crud_favorite.add_toilet(db, user.user_id, user.toilet_id) == "Toilet added sucessfully":
        return {"message": "Toilet added sucessfully"}

@router.post("/delList")
def del_favorite(
    user: favorite_schema.FavoriteDel,
    db: Session = Depends(get_db)
):
    if crud_favorite.del_toilet(db, user.id) == "Toilet deleted sucessfully":
        return {"message": "Toilet deleted sucessfully"}