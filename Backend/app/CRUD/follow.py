from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import follow as schemas

# 新增追蹤紀錄
def create_follow(db: Session, follow: schemas.FollowCreate):
    """新增追蹤紀錄"""
    insert_query = text("""
        INSERT INTO follow (following_id, followed_id)
        VALUES (:following_id, :followed_id)
    """)
    result = db.execute(insert_query, {
        "following_id": follow.following_id,
        "followed_id": follow.followed_id
    })
    db.commit()
    
    inserted_id = result.lastrowid
    select_query = text("SELECT * FROM follow WHERE id = :id")
    row = db.execute(select_query, {"id": inserted_id}).fetchone()

    if row:
        return dict(row._mapping)
    return None

# 根據使用者查詢他正在追蹤的人
def get_following_user(db: Session, following_id: int):
    """取得使用者正在追蹤的人清單"""
    query = text("SELECT * FROM follow WHERE following_id = :following_id")
    rows = db.execute(query, {"following_id": following_id}).fetchall()
    return [dict(row._mapping) for row in rows]

# 根據使用者查詢他被誰追蹤
def get_follower(db: Session, followed_id: int):
    """取得追蹤該使用者的人的清單"""
    query = text("SELECT * FROM follow WHERE followed_id = :followed_id")
    rows = db.execute(query, {"followed_id": followed_id}).fetchall()
    return [dict(row._mapping) for row in rows]

# 取消追蹤
def unfollow(db: Session, followed_id: int, following_id: int):
    """取消追蹤"""
    check_query = text("""
        SELECT * FROM follow 
        WHERE followed_id = :followed_id AND following_id = :following_id
        LIMIT 1
    """)
    row = db.execute(check_query, {
        "followed_id": followed_id,
        "following_id": following_id
    }).fetchone()
    
    if row is None:
        return None

    delete_query = text("""
        DELETE FROM follow 
        WHERE followed_id = :followed_id AND following_id = :following_id
    """)
    db.execute(delete_query, {
        "followed_id": followed_id,
        "following_id": following_id
    })
    db.commit()

    return dict(row._mapping)
