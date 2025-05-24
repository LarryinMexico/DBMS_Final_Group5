from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import reaction as schemas

# 新增 reaction
def create_reaction(db: Session, reaction: schemas.ReactionCreate):
    """創建新反應"""
    reaction_data = reaction.dict()
    
    # 動態構建插入語句
    columns = list(reaction_data.keys())
    placeholders = [f":{col}" for col in columns]
    
    insert_query = text(f"""
        INSERT INTO reaction ({', '.join(columns)}) 
        VALUES ({', '.join(placeholders)})
    """)
    
    # 執行插入
    result = db.execute(insert_query, reaction_data)
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM reaction WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None

# 查詢 reaction
def get_per_reaction(db: Session, reaction_id: int):
    """根據 ID 獲取單個反應"""
    query = text("SELECT * FROM reaction WHERE id = :reaction_id")
    result = db.execute(query, {"reaction_id": reaction_id})
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None

def get_multi_by_review(db: Session, review_id: int, skip: int = 0, limit: int = 100):
    """根據評論 ID 獲取多個反應（支援分頁）"""
    query = text("""
        SELECT * FROM reaction 
        WHERE review_id = :review_id 
        LIMIT :limit OFFSET :skip
    """)
    result = db.execute(query, {"review_id": review_id, "limit": limit, "skip": skip})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_multi_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """根據用戶 ID 獲取多個反應（支援分頁）"""
    query = text("""
        SELECT * FROM reaction 
        WHERE user_id = :user_id 
        LIMIT :limit OFFSET :skip
    """)
    result = db.execute(query, {"user_id": user_id, "limit": limit, "skip": skip})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

# 修改 reaction
def update_reaction(db: Session, reaction_id: int, reaction_update: schemas.ReactionUpdate):
    """更新反應"""
    # 先檢查記錄是否存在
    existing_reaction = get_per_reaction(db, reaction_id)
    if not existing_reaction:
        return None
    
    # 獲取需要更新的欄位（排除未設置的欄位）
    update_data = reaction_update.dict(exclude_unset=True)
    if not update_data:
        return existing_reaction
    
    # 動態構建更新語句
    set_clauses = [f"{col} = :{col}" for col in update_data.keys()]
    update_query = text(f"""
        UPDATE reaction 
        SET {', '.join(set_clauses)}
        WHERE id = :reaction_id
    """)
    
    # 加入 reaction_id 到參數中
    update_data['reaction_id'] = reaction_id
    
    # 執行更新
    db.execute(update_query, update_data)
    db.commit()
    
    # 查詢更新後的記錄
    return get_per_reaction(db, reaction_id)

# 刪除 reaction
def delete_reaction(db: Session, reaction_id: int):
    """刪除反應"""
    # 先檢查記錄是否存在
    existing_reaction = get_per_reaction(db, reaction_id)
    if not existing_reaction:
        return False
    
    # 執行刪除
    delete_query = text("DELETE FROM reaction WHERE id = :reaction_id")
    db.execute(delete_query, {"reaction_id": reaction_id})
    db.commit()
    
    return True