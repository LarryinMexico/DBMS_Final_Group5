from sqlalchemy.orm import Session
from app.models import reaction as models
from app.schemas import reaction as schemas

#新增 reaction
def create_reaction(db: Session, reaction: schemas.ReactionCreate):
    db_reaction = models.Reaction(**reaction.dict())
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

#查詢 reaction
def get_per_reaction(db: Session, reaction_id: int):
    return db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()

def get_multi_by_review(db: Session, review_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Reaction).filter(models.Reaction.review_id == review_id).offset(skip).limit(limit).all()

def get_multi_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Reaction).filter(models.Reaction.user_id == user_id).offset(skip).limit(limit).all()

#修改 reaction
def update_reaction(db: Session, reaction: models.Reaction, reaction_update: schemas.ReactionUpdate):
    for key, value in reaction_update.dict(exclude_unset=True).items():
        setattr(reaction, key, value)
    db.commit()
    db.refresh(reaction)
    return reaction

#刪除 reaction
def delete_reaction(db: Session, reaction_id: int):
    db_reaction = db.query(models.Reaction).filter(models.Reaction.id == reaction_id).first()
    if db_reaction:
        db.delete(db_reaction)
        db.commit()
        return True
    return False