from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.CRUD import toilet as crud_toilet
from app.CRUD import amenity as crud_amenity
from app.schemas import amenity as schemas
from app.db.security import verify_jwt  # Clerk JWT 驗證

router = APIRouter()

# 新增廁所設施
@router.post("/", response_model=schemas.Amenity)
async def create_amenity(
    amenity: schemas.AmenityCreate,
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    新增設施類型（需驗證 JWT）
    """
    return crud_amenity.create_amenity(db, amenity)

# 取得設施
@router.get("/{amenity_id}", response_model=schemas.Amenity)
async def get_amenity(
    amenity_id: int = Path(..., description="設施 ID"),
    db: Session = Depends(get_db)
):
    """
    取得特定設施資訊
    """
    amenity = crud_amenity.get_amenity(db, amenity_id)
    if not amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return amenity

# 獲取所有設施
@router.get("/", response_model=List[schemas.Amenity])
async def list_amenities(
    skip: int = Query(0, description="跳過的紀錄數"),
    limit: int = Query(100, description="返回的最大紀錄數"),
    db: Session = Depends(get_db)
):
    """
    🔍 顯示所有設施類型（可分頁）
    """
    return crud_amenity.get_amenities(db, skip, limit)

# 刪除某個設施
@router.delete("/{amenity_id}")
async def delete_amenity(
    amenity_id: int = Path(..., description="設施 ID"),
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    刪除設施類型（需驗證 JWT）
    """
    success = crud_amenity.delete_amenity(db, amenity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Amenity not found")
    return {"message": "Amenity successfully deleted"}

# 用toilet_id或是amenity_id獲取amenity
@router.post("/toilet/{toilet_id}/amenity/{amenity_id}")
async def add_amenity_to_toilet(
    toilet_id: int = Path(..., description="廁所 ID"),
    amenity_id: int = Path(..., description="設施 ID"),
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    為廁所新增設施（需驗證 JWT）
    """
    toilet = crud_toilet.add_amenity_to_toilet(db, toilet_id, amenity_id)
    if not toilet:
        raise HTTPException(status_code=404, detail="Toilet or Amenity not found")
    return {"message": "Amenity added to toilet successfully"}

# 用toilet_id或是amenity_id刪除amenity
@router.delete("/toilet/{toilet_id}/amenity/{amenity_id}")
async def remove_amenity_from_toilet(
    toilet_id: int = Path(..., description="廁所 ID"),
    amenity_id: int = Path(..., description="設施 ID"),
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    移除廁所的設施（需驗證 JWT）
    """
    toilet = crud_toilet.remove_amenity_from_toilet(db, toilet_id, amenity_id)
    if not toilet:
        raise HTTPException(status_code=404, detail="Toilet or Amenity not found or Amenity is not associated with this toilet")
    return {"message": "Amenity removed from toilet successfully"}

# 取得特定廁所的所有設施
@router.get("/toilet/{toilet_id}/amenities", response_model=List[schemas.Amenity])
async def get_toilet_amenities(
    toilet_id: int = Path(..., description="廁所 ID"),
    db: Session = Depends(get_db)
):
    """
    取得特定廁所的所有設施
    """
    toilet = crud_toilet.get_toilet_by_id(db, toilet_id)
    if not toilet:
        raise HTTPException(status_code=404, detail="Toilet not found")
    return toilet.amenities