from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import reaction as reaction_schemas
from app.CRUD import reaction as reaction_crud
from app.db.session import get_db
from typing import List

router = APIRouter()

# 新增 reaction
@router.post("/reactions/", response_model=reaction_schemas.ReactionOut)
def create_reaction(reaction_in: reaction_schemas.ReactionCreate, db: Session = Depends(get_db)):
    return reaction_crud.create_reaction(db=db, reaction=reaction_in)

# 查詢 reaction by ID
@router.get("/reactions/{reaction_id}", response_model=reaction_schemas.ReactionOut)
def get_reaction(reaction_id: int, db: Session = Depends(get_db)):
    db_reaction = reaction_crud.get_per_reaction(db=db, reaction_id=reaction_id)
    return db_reaction

# 查詢 reactions by review ID
@router.get("/reviews/{review_id}/reactions/", response_model=List[reaction_schemas.ReactionOut])
def get_review_reactions(review_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reaction_crud.get_multi_by_review(db=db, review_id=review_id, skip=skip, limit=limit)

# 查詢 reactions by user ID
@router.get("/users/{user_id}/reactions/", response_model=List[reaction_schemas.ReactionOut])
def get_user_reactions(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return reaction_crud.get_multi_by_user(db=db, user_id=user_id, skip=skip, limit=limit)

# 修改 reaction by ID
@router.put("/reactions/{reaction_id}", response_model=reaction_schemas.ReactionOut)
def update_reaction(reaction_id: int, reaction_in: reaction_schemas.ReactionUpdate, db: Session = Depends(get_db)):
    db_reaction = reaction_crud.get_per_reaction(db=db, reaction_id=reaction_id)
    if not db_reaction:
        return False
    return reaction_crud.update_reaction(db=db, db_reaction=db_reaction, reaction_update=reaction_in)

# 刪除 reaction by ID
@router.delete("/reactions/{reaction_id}", response_model=dict)
def delete_reaction(reaction_id: int, db: Session = Depends(get_db)):
    if not reaction_crud.delete_reaction(db=db, reaction_id=reaction_id):
        return False
    return True