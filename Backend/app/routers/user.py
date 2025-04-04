# app/routers/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.CRUD import user as crud_user
from app.schemas import user as user_schema
from app.db.session import get_db
from app.db.security import verify_jwt  # Clerk JWT 驗證

router = APIRouter()


@router.post("/", response_model=user_schema.UserOut)
async def register_user(
    user_data: user_schema.UserCreate,
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    註冊新使用者（需驗證 JWT）
    """
    clerk_id = clerk_user["sub"]

    # 檢查是否已註冊
    existing_user = crud_user.get_user_by_clerk_id(db, clerk_id)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # 建立新使用者
    return crud_user.create_user(
        db,
        user_schema.UserCreate(
            clerk_id=clerk_id,
            name=user_data.name,
            email=user_data.email,
        )
    )


@router.get("/me", response_model=user_schema.UserOut)
async def get_current_user(
    db: Session = Depends(get_db),
    clerk_user: dict = Depends(verify_jwt)
):
    """
    取得目前登入的使用者資訊（需驗證 JWT）
    """
    user = crud_user.get_user_by_clerk_id(db, clerk_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[user_schema.UserOut])
def list_users(db: Session = Depends(get_db)):
    """
    🔍 顯示所有使用者（測試用）
    """
    return crud_user.get_all_users(db)
