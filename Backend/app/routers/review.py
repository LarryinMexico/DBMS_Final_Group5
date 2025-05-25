from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import review as review_schemas
from app.CRUD import review as review_crud
from app.db.session import get_db
from app.models.review import Review
from typing import List
from sqlalchemy import func
from app.socketio import sio 

router = APIRouter()

#新增 review
@router.post("/", response_model = review_schemas.ReviewOut)
async def create_review(review: review_schemas.ReviewCreate, db: Session=Depends(get_db)):
    created = review_crud.create_review(db,review)
    print("created", created)
    await sio.emit("comment-received", {
        "toiletId": created["toilet_id"],
        "user": created["user_id"],
        "comment": created["comment"],
        "rating": created["rating"],
    })

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

@router.get("/user/{user_id}/full")
def get_full_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    回傳該使用者的所有評論，附帶使用者資訊、廁所名稱與 reactions 數量。
    """
    from sqlalchemy import text

    query = text("""
        SELECT r.id, r.rating, r.comment, r.updateAt,
            u.id AS user_id, u.name AS user_name, u.avatarUrl,
            t.id AS toilet_id, t.title AS toilet_title,
            (SELECT COUNT(*) FROM reaction WHERE review_id = r.id) AS reactions_count
        FROM review r
        JOIN `users` u ON r.user_id = u.id
        JOIN toilet t ON r.toilet_id = t.id
        WHERE r.user_id = :user_id
        ORDER BY r.updateAt DESC
    """)

    result = db.execute(query, {"user_id": user_id})
    rows = result.fetchall()

    return [
        {
            "id": row.id,
            "rating": row.rating,
            "comment": row.comment,
            "updateAt": row.updateAt,
            "toilet": {
                "id": row.toilet_id,
                "title": row.toilet_title,
            },
            "user": {
                "id": row.user_id,
                "name": row.user_name,
                "avatarUrl": row.avatarUrl,
            },
            "reactionsCount": row.reactions_count,
        }
        for row in rows
    ]
