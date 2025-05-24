from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import review as schemas

# 新增 review
def create_review(db: Session, review: schemas.ReviewCreate):
    """創建新評論"""
    review_data = review.dict()
    
    # 動態構建插入語句
    columns = list(review_data.keys())
    placeholders = [f":{col}" for col in columns]
    
    insert_query = text(f"""
        INSERT INTO review ({', '.join(columns)}) 
        VALUES ({', '.join(placeholders)})
    """)
    
    # 執行插入
    result = db.execute(insert_query, review_data)
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM review WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None

# 修改 review
def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate):
    """更新評論"""
    # 先檢查記錄是否存在
    check_query = text("SELECT * FROM review WHERE id = :review_id")
    result = db.execute(check_query, {"review_id": review_id})
    existing_review = result.fetchone()
    
    if existing_review is None:
        return False
    
    # 獲取需要更新的欄位（排除未設置的欄位）
    update_data = review_update.dict(exclude_unset=True)
    if not update_data:
        return dict(existing_review._mapping)
    
    # 動態構建更新語句
    set_clauses = [f"{col} = :{col}" for col in update_data.keys()]
    update_query = text(f"""
        UPDATE review 
        SET {', '.join(set_clauses)}
        WHERE id = :review_id
    """)
    
    # 加入 review_id 到參數中
    update_data['review_id'] = review_id
    
    # 執行更新
    db.execute(update_query, update_data)
    db.commit()
    
    # 查詢更新後的記錄
    result = db.execute(check_query, {"review_id": review_id})
    updated_row = result.fetchone()
    
    if updated_row:
        return dict(updated_row._mapping)
    return False

# 刪除 review
def delete_review(db: Session, review_id: int):
    """刪除評論"""
    # 先檢查記錄是否存在
    check_query = text("SELECT id FROM review WHERE id = :review_id")
    result = db.execute(check_query, {"review_id": review_id})
    existing_review = result.fetchone()
    
    if existing_review is None:
        return False
    
    # 執行刪除
    delete_query = text("DELETE FROM review WHERE id = :review_id")
    db.execute(delete_query, {"review_id": review_id})
    db.commit()
    
    return True

# 查詢 review by user_id
def get_review_by_user(db: Session, user_id: int):
    """根據用戶 ID 獲取所有評論"""
    query = text("SELECT * FROM review WHERE user_id = :user_id")
    result = db.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

# 查詢 review by toilet_id
def get_review_by_toilet(db: Session, toilet_id: int):
    """根據廁所 ID 獲取所有評論"""
    query = text("SELECT * FROM review WHERE toilet_id = :toilet_id")
    result = db.execute(query, {"toilet_id": toilet_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]