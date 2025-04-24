from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import reaction as reaction_schemas
from app.CRUD import reaction as reaction_crud
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=reaction_schemas.ReactionOut)
def create_reaction(
    reaction_in: reaction_schemas.ReactionCreate,
    db: Session = Depends(get_db)
):
    """
    建立新的 Reaction。

    - **user_id**: 使用者 ID
    - **review_id**: 所屬評論 ID
    """
    return reaction_crud.create_reaction(db=db, reaction=reaction_in)


@router.get("/{reaction_id}", response_model=reaction_schemas.ReactionOut)
def get_reaction(
    reaction_id: int,
    db: Session = Depends(get_db)
):
    """
    根據 reaction ID 取得單一 reaction。
    """
    db_reaction = reaction_crud.get_per_reaction(db=db, reaction_id=reaction_id)
    if not db_reaction:
        raise HTTPException(status_code=404, detail="Reaction not found")
    return db_reaction


@router.get("/review/{review_id}", response_model=List[reaction_schemas.ReactionOut])
def get_review_reactions(
    review_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    根據評論 ID 查詢所有 reactions。

    - 可設定 `skip` 與 `limit` 分頁查詢
    """
    return reaction_crud.get_multi_by_review(db=db, review_id=review_id, skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[reaction_schemas.ReactionOut])
def get_user_reactions(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    根據使用者 ID 查詢其所有 reactions。

    - 可設定 `skip` 與 `limit` 分頁查詢
    """
    return reaction_crud.get_multi_by_user(db=db, user_id=user_id, skip=skip, limit=limit)


@router.delete("/{reaction_id}")
def delete_reaction(
    reaction_id: int,
    db: Session = Depends(get_db)
):
    """
    根據 reaction ID 刪除 reaction。
    """
    success = reaction_crud.delete_reaction(db=db, reaction_id=reaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reaction not found or already deleted")
    return {"message": "Reaction deleted successfully"}