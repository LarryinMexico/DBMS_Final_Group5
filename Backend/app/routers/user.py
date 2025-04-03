from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.CRUD import user as crud_user
from app.schemas import user as user_schema
from app.db.session import SessionLocal

router = APIRouter()

# Dependency: get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[user_schema.UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_all_users(db)

@router.post("/", response_model=user_schema.UserOut)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)
