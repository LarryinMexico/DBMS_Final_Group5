from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import toilet as schemas

def get_toilet_by_id(db: Session, toilet_id: int):
    """根據 ID 獲取廁所"""
    query = text("SELECT * FROM toilet WHERE id = :toilet_id")
    result = db.execute(query, {"toilet_id": toilet_id})
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None

def get_toilets_by_building_id(db: Session, building_id: int):
    """根據建築物 ID 獲取所有廁所"""
    query = text("SELECT * FROM toilet WHERE building_id = :building_id")
    result = db.execute(query, {"building_id": building_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_toilets_by_floor(db: Session, building_id: int, floor: int):
    """根據建築物 ID 和樓層獲取廁所"""
    query = text("""
        SELECT * FROM toilet 
        WHERE building_id = :building_id AND floor = :floor
    """)
    result = db.execute(query, {"building_id": building_id, "floor": floor})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def get_all_toilets(db: Session, skip: int = 0, limit: int = 100):
    """獲取所有廁所（支援分頁）"""
    query = text("SELECT * FROM toilet LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

def create_toilet(db: Session, toilet: schemas.ToiletCreate):
    """創建新廁所"""
    toilet_data = toilet.dict()
    
    # 動態構建插入語句
    columns = list(toilet_data.keys())
    placeholders = [f":{col}" for col in columns]
    
    insert_query = text(f"""
        INSERT INTO toilet ({', '.join(columns)}) 
        VALUES ({', '.join(placeholders)})
    """)
    
    # 執行插入
    result = db.execute(insert_query, toilet_data)
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM toilet WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None

def update_toilet(db: Session, toilet_id: int, toilet: schemas.ToiletUpdate):
    """更新廁所資訊"""
    # 先檢查記錄是否存在
    existing_toilet = get_toilet_by_id(db, toilet_id)
    if not existing_toilet:
        return None
    
    # 獲取需要更新的欄位（排除未設置的欄位）
    update_data = toilet.dict(exclude_unset=True)
    if not update_data:
        return existing_toilet
    
    # 動態構建更新語句
    set_clauses = [f"{col} = :{col}" for col in update_data.keys()]
    update_query = text(f"""
        UPDATE toilet 
        SET {', '.join(set_clauses)}
        WHERE id = :toilet_id
    """)
    
    # 加入 toilet_id 到參數中
    update_data['toilet_id'] = toilet_id
    
    # 執行更新
    db.execute(update_query, update_data)
    db.commit()
    
    # 查詢更新後的記錄
    return get_toilet_by_id(db, toilet_id)

def delete_toilet(db: Session, toilet_id: int):
    """刪除廁所"""
    # 先檢查記錄是否存在
    existing_toilet = get_toilet_by_id(db, toilet_id)
    if not existing_toilet:
        return False
    
    # 執行刪除
    delete_query = text("DELETE FROM toilet WHERE id = :toilet_id")
    db.execute(delete_query, {"toilet_id": toilet_id})
    db.commit()
    
    return True

def add_amenity_to_toilet(db: Session, toilet_id: int, amenity_id: int):
    from app.models.amenity import Amenity
    toilet = get_toilet_by_id(db, toilet_id)
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity:
        toilet.amenities.append(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None

def remove_amenity_from_toilet(db: Session, toilet_id: int, amenity_id: int):
    from app.models.amenity import Amenity
    toilet = get_toilet_by_id(db, toilet_id)
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity and amenity in toilet.amenities:
        toilet.amenities.remove(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None
