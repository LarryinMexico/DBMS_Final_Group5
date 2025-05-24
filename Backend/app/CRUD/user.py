from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import user as schemas

def get_user_by_clerk_id(db: Session, clerk_id: str):
    """根據 clerk_id 獲取用戶"""
    query = text("SELECT * FROM users WHERE clerk_id = :clerk_id")
    result = db.execute(query, {"clerk_id": clerk_id})
    row = result.fetchone()
    if row:
        # 將結果轉換為字典格式
        return dict(row._mapping)
    return None

def get_all_users(db: Session):
    """獲取所有用戶"""
    query = text("SELECT * FROM users")
    result = db.execute(query)
    rows = result.fetchall()
    # 將所有結果轉換為字典列表
    return [dict(row._mapping) for row in rows]

def create_user(db: Session, user: schemas.UserCreate):
    """創建新用戶"""
    user_data = user.dict()
    
    # 動態構建插入語句
    columns = list(user_data.keys())
    placeholders = [f":{col}" for col in columns]
    
    insert_query = text(f"""
        INSERT INTO users ({', '.join(columns)}) 
        VALUES ({', '.join(placeholders)})
    """)
    
    # 執行插入
    result = db.execute(insert_query, user_data)
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM users WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None