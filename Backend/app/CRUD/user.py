from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas import user as schemas

def get_user_by_clerk_id(db: Session, clerk_id: str):
    return db.query(models.User).filter(models.User.clerk_id == clerk_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user