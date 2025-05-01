from sqlalchemy.orm import Session
from app.models import follow as models
from app.models import user as user
from app.schemas import follow as schemas

#開始追蹤，新增一筆追蹤的資料
def create_follow(db: Session, follow: schemas.FollowCreate):
    db_follow = models.Follow(**follow.dict())
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


#查詢追蹤的人的清單
def get_following_user(db: Session, following_id: int):
    return db.query(models.Follow).filter(models.Follow.id == following_id).all()

#查詢被誰追蹤的清單
def get_follower(db: Session, followed_id: int):
    return db.query(models.Follow).filter(models.Follow.id == followed_id).all()

#取消追蹤
def unfollow(db: Session, followed_id: int, following_id: int):
    follow = db.query(models.Follow).filter_by(
        followed_id=followed_id,
        following_id=following_id
    ).first()
    if follow:
        db.delete(follow)
        db.commit()
    return follow

