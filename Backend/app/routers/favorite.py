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
    return crud_favorite.get_favorite_list(db, user.UserID)
