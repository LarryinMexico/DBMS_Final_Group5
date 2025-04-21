from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.CRUD import favorite as crud_favorite
from app.schemas import favorite as favorite_schema
from app.db.session import get_db
from typing import List

router = APIRouter()

@router.get("/list/{user_id}")
def list_favorite(
    user_id: int,
    db: Session = Depends(get_db)
):
    return crud_favorite.get_favorite_list(db, user_id)

@router.post("/add")
def add_favorite(
    user: favorite_schema.FavoriteAdd,
    db: Session = Depends(get_db)
):
    if crud_favorite.add_toilet(db, user.user_id, user.toilet_id) == "Toilet added sucessfully":
        return {"message": "Toilet added sucessfully"}

@router.delete("/delete/{id}")
def del_favorite(
    id: int,
    db: Session = Depends(get_db)
):
    if crud_favorite.del_toilet(db, id) == "Toilet deleted sucessfully":
        return {"message": "Toilet deleted sucessfully"}