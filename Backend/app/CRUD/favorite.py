from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import favorite as schemas

def get_favorite_list(db: Session, user_id: int):
    """獲取用戶的收藏列表"""
    query = text("SELECT * FROM favorite WHERE user_id = :user_id")
    result = db.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def add_toilet(db: Session, input_user_id: int, input_toilet_id: int):
    """新增廁所到收藏"""
    # 檢查是否已經收藏過
    check_query = text("""
        SELECT id FROM favorite 
        WHERE user_id = :user_id AND toilet_id = :toilet_id
    """)
    result = db.execute(check_query, {"user_id": input_user_id, "toilet_id": input_toilet_id})
    existing = result.fetchone()
    
    if existing:
        return "Toilet already in favorites"
    
    # 插入新的收藏記錄
    insert_query = text("""
        INSERT INTO favorite (user_id, toilet_id) 
        VALUES (:user_id, :toilet_id)
    """)
    
    db.execute(insert_query, {"user_id": input_user_id, "toilet_id": input_toilet_id})
    db.commit()
    
    return "Toilet added sucessfully"

def del_toilet(db: Session, user_id: int, toilet_id: int):
    """從收藏中刪除廁所"""
    # 先檢查記錄是否存在
    check_query = text("""
        SELECT id FROM favorite 
        WHERE user_id = :user_id AND toilet_id = :toilet_id
    """)
    result = db.execute(check_query, {"user_id": user_id, "toilet_id": toilet_id})
    existing = result.fetchone()
    
    if not existing:
        return False
    
    # 執行刪除
    delete_query = text("""
        DELETE FROM favorite 
        WHERE user_id = :user_id AND toilet_id = :toilet_id
    """)
    db.execute(delete_query, {"user_id": user_id, "toilet_id": toilet_id})
    db.commit()
    
    return True

