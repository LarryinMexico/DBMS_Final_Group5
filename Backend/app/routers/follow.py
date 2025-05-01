from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.session import SessionLocal
from app.schemas import follow as follow_schemas
from app.CRUD import follow as follow_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#開始追蹤，新增一筆追蹤的資料
@router.post("/", response_model=follow_schemas.FollowOut)
def create_follow(follow: follow_schemas.FollowCreate, db: Session = Depends(get_db)):
    return follow_crud.create_follow(db, follow)

#取消追蹤
@router.delete("/", status_code=204)
def unfollow(follower_id: int, followed_id: int, db: Session = Depends(get_db)):
    follow = follow_crud.unfollow(db, followed_id=followed_id, following_id=follower_id)
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")

#查詢追蹤的人的清單
@router.get("/following/{follower_id}", response_model=list[follow_schemas.FollowOut])
def get_following_user(follower_id: int, db: Session = Depends(get_db)):
    return follow_crud.get_following_user(db, following_id=follower_id)

#查詢被誰追蹤的清單
@router.get("/followers/{followed_id}", response_model=list[follow_schemas.FollowOut])
def get_follower(followed_id: int, db: Session = Depends(get_db)):
    return follow_crud.get_follower(db, followed_id=followed_id)
