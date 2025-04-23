from sqlalchemy.orm import Session
from app.models import review as models
from app.schemas import review as schemas

#新增 review
def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

#修改 review
def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate):
    review_old = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if review_old is None:
        return False
    
    update_data = review_update.dict(exclude_unset=True)
    for key,value in update_data.items():
        setattr(review_old,key,value)
    db.commit()
    db.refresh(review_old)
    return review_old


#刪除 review
def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.review_id == review_id).first()
    if review is None:
        return False
    db.delete(review)
    db.commit()
    return True

#查詢 review by user_id
def get_review_by_user(db: Session, user_id: int):
    return db.query(models.Review).filter(models.Review.user_id == user_id).all()

#查詢 review by toilet_id
def get_review_by_toilet(db: Session, toilet_id: int):
    return db.query(models.Review).filter(models.Review.toilet_id == toilet_id).all()
