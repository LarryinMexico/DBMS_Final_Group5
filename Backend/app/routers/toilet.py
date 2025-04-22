# app/routers/toilet.py

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.CRUD import toilet as crud_toilet
from app.schemas import toilet as toilet_schema
from app.db.session import get_db
from app.db.security import verify_jwt  # Clerk JWT 驗證

router = APIRouter()

@router.post("/", response_model=toilet_schema.ToiletOut)
async def create_toilet(
    toilet_data: toilet_schema.ToiletCreate,
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    新增廁所資訊（需驗證 JWT）
    """
    return crud_toilet.create_toilet(db, toilet_data)

@router.get("/{toilet_id}", response_model=toilet_schema.ToiletOut)
async def get_toilet(
    toilet_id: int = Path(..., description="廁所 ID"),
    db: Session = Depends(get_db)
):
    """
    取得特定廁所資訊
    """
    toilet = crud_toilet.get_toilet_by_id(db, toilet_id)
    if not toilet:
        raise HTTPException(status_code=404, detail="Toilet not found")
    return toilet

@router.get("/building/{building_id}", response_model=list[toilet_schema.ToiletOut])
async def get_toilets_by_building(
    building_id: int = Path(..., description="建築物 ID"),
    db: Session = Depends(get_db)
):
    """
    取得特定建築物的所有廁所資訊
    """
    return crud_toilet.get_toilets_by_building_id(db, building_id)

@router.get("/building/{building_id}/floor/{floor}", response_model=list[toilet_schema.ToiletOut])
async def get_toilets_by_floor(
    building_id: int = Path(..., description="建築物 ID"),
    floor: int = Path(..., description="樓層"),
    db: Session = Depends(get_db)
):
    """
    取得特定建築物特定樓層的廁所資訊
    """
    return crud_toilet.get_toilets_by_floor(db, building_id, floor)

@router.get("/", response_model=list[toilet_schema.ToiletOut])
async def list_toilets(
    skip: int = Query(0, description="跳過的紀錄數"),
    limit: int = Query(100, description="返回的最大紀錄數"),
    db: Session = Depends(get_db)
):
    """
    🔍 顯示所有廁所資訊（可分頁）
    """
    return crud_toilet.get_all_toilets(db, skip, limit)

@router.put("/{toilet_id}", response_model=toilet_schema.ToiletOut)
async def update_toilet(
    toilet_id: int = Path(..., description="廁所 ID"),
    toilet_data: toilet_schema.ToiletUpdate = None,
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    更新廁所資訊（需驗證 JWT）
    """
    toilet = crud_toilet.update_toilet(db, toilet_id, toilet_data)
    if not toilet:
        raise HTTPException(status_code=404, detail="Toilet not found")
    return toilet

@router.delete("/{toilet_id}")
async def delete_toilet(
    toilet_id: int = Path(..., description="廁所 ID"),
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    刪除廁所資訊（需驗證 JWT）
    """
    success = crud_toilet.delete_toilet(db, toilet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Toilet not found")
    return {"message": "Toilet successfully deleted"}