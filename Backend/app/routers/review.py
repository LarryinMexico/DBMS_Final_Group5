from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import review as review_schemas
from app.CRUD import review as review_crud
from app.db.session import get_db
from app.models.review import Review
from typing import List
from sqlalchemy import func

router = APIRouter()

#新增 review
@router.post("/", response_model = review_schemas.ReviewOut)
def create_review(review: review_schemas.ReviewCreate, db: Session=Depends(get_db)):
    created = review_crud.create_review(db,review)
    return created

#修改 review
@router.put("/{review_id}")
def update_review(review_id: int, review: review_schemas.ReviewUpdate, db: Session=Depends(get_db)):
    updated_review = review_crud.update_review(db,review_id,review)
    if updated_review is None:
        return False
    return updated_review

#刪除 review
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session=Depends(get_db)):
    return review_crud.delete_review(db,review_id)

#查詢 review by user_id
@router.get("/user/{user_id}",response_model=list[review_schemas.ReviewOut])
def get_reviews_by_user(user_id: int, db: Session=Depends(get_db)):
    return review_crud.get_review_by_user(db,user_id)

#查詢 review by toilet_id
@router.get("/toilet/{toilet_id}",response_model=list[review_schemas.ReviewOut])
def get_review_by_toilet(toilet_id: int, db: Session=Depends(get_db)):
    return review_crud.get_review_by_toilet(db,toilet_id)

@router.get("/stats", response_model=List[review_schemas.ReviewStat])
def get_review_stats(db: Session = Depends(get_db)):
    """
    取得每個廁所的平均評分與評論數量。
    """
    results = (
        db.query(
            Review.toilet_id,
            func.avg(Review.rating).label("avg_rating"),
            func.count(Review.id).label("count")
        )
        .group_by(Review.toilet_id)
        .all()
    )

    return [
        {
            "toilet_id": row.toilet_id,
            "avg_rating": round(row.avg_rating, 1),
            "count": row.count
        }
        for row in results
    ]