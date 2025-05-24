from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import building as schemas

def get_building(db: Session, building_id: int):
    """根據 ID 獲取建築物"""
    query = text("SELECT * FROM building WHERE id = :building_id")
    result = db.execute(query, {"building_id": building_id})
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None

def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    """獲取所有建築物（支援分頁）"""
    query = text("SELECT * FROM building LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def create_building(db: Session, building: schemas.BuildingCreate):
    """創建新建築物"""
    building_data = building.dict()
    
    # 動態構建插入語句
    columns = list(building_data.keys())
    placeholders = [f":{col}" for col in columns]
    
    insert_query = text(f"""
        INSERT INTO building ({', '.join(columns)}) 
        VALUES ({', '.join(placeholders)})
    """)
    
    # 執行插入
    result = db.execute(insert_query, building_data)
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM building WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None

def update_building(db: Session, building_id: int, building: schemas.BuildingCreate):
    """更新建築物資訊"""
    # 先檢查記錄是否存在
    existing_building = get_building(db, building_id)
    if not existing_building:
        return None
    
    # 獲取需要更新的欄位
    update_data = building.dict()
    if not update_data:
        return existing_building
    
    # 動態構建更新語句
    set_clauses = [f"{col} = :{col}" for col in update_data.keys()]
    update_query = text(f"""
        UPDATE building 
        SET {', '.join(set_clauses)}
        WHERE id = :building_id
    """)
    
    # 加入 building_id 到參數中
    update_data['building_id'] = building_id
    
    # 執行更新
    db.execute(update_query, update_data)
    db.commit()
    
    # 查詢更新後的記錄
    return get_building(db, building_id)

def delete_building(db: Session, building_id: int):
    """刪除建築物"""
    # 先檢查記錄是否存在
    existing_building = get_building(db, building_id)
    if not existing_building:
        return False
    
    # 執行刪除
    delete_query = text("DELETE FROM building WHERE id = :building_id")
    db.execute(delete_query, {"building_id": building_id})
    db.commit()
    
    return True