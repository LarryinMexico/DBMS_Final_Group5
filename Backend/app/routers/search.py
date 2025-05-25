from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import search as schemas
from app.CRUD import search as crud
from app.db.session import get_db

router = APIRouter(
    prefix="/toilets",
    tags=["Toilets"]
)

@router.post("/search")
def search_toilets_endpoint(
    filters: schemas.Search,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    根據條件搜尋符合的廁所。
    """
    return crud.search_toilets(db=db, filters=filters, skip=skip, limit=limit)
