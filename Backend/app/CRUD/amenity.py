from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import amenity as schemas

# 取得單一 amenity
def get_amenity(db: Session, amenity_id: int):
    sql = "SELECT * FROM amenity WHERE id = :amenity_id LIMIT 1"
    row = db.execute(text(sql), {"amenity_id": amenity_id}).fetchone()
    return dict(row._mapping) if row else None

# 取得多個 amenities（支援分頁）
def get_amenities(db: Session, skip: int = 0, limit: int = 100):
    sql = "SELECT * FROM amenity LIMIT :limit OFFSET :skip"
    rows = db.execute(text(sql), {"skip": skip, "limit": limit}).fetchall()
    return [dict(row._mapping) for row in rows]

# 新增 amenity
def create_amenity(db: Session, amenity: schemas.AmenityCreate):
    insert_query = text("""
        INSERT INTO amenity (name)
        VALUES (:name)
    """)
    result = db.execute(insert_query, {
        "name": amenity.name,
    })
    db.commit()

    inserted_id = result.lastrowid
    select_query = text("SELECT * FROM amenity WHERE id = :id")
    row = db.execute(select_query, {"id": inserted_id}).fetchone()

    return dict(row._mapping) if row else None

# 刪除 amenity
def delete_amenity(db: Session, amenity_id: int):
    check_query = text("SELECT id FROM amenity WHERE id = :amenity_id")
    row = db.execute(check_query, {"amenity_id": amenity_id}).fetchone()

    if not row:
        return False

    delete_query = text("DELETE FROM amenity WHERE id = :amenity_id")
    db.execute(delete_query, {"amenity_id": amenity_id})
    db.commit()
    return True

# 將 amenity 加入到指定 toilet
def add_amenity_to_toilet(db: Session, toilet_id: int, amenity_id: int):
    # 檢查 toilet 和 amenity 是否存在
    toilet_exists = db.execute(
        text("SELECT id FROM toilet WHERE id = :id"), {"id": toilet_id}
    ).fetchone()
    amenity_exists = db.execute(
        text("SELECT id FROM amenity WHERE id = :id"), {"id": amenity_id}
    ).fetchone()

    if not toilet_exists or not amenity_exists:
        return None

    # 檢查是否已存在關係
    relation_exists = db.execute(
        text("SELECT 1 FROM has WHERE toilet_id = :toilet_id AND amenity_id = :amenity_id"),
        {"toilet_id": toilet_id, "amenity_id": amenity_id}
    ).fetchone()

    if not relation_exists:
        db.execute(
            text("INSERT INTO has (toilet_id, amenity_id) VALUES (:toilet_id, :amenity_id)"),
            {"toilet_id": toilet_id, "amenity_id": amenity_id}
        )
        db.commit()

    # 回傳該廁所最新資料
    row = db.execute(
        text("SELECT * FROM toilet WHERE id = :id"), {"id": toilet_id}
    ).fetchone()

    return dict(row._mapping) if row else None

# 將 amenity 從指定 toilet 移除
def remove_amenity_from_toilet(db: Session, toilet_id: int, amenity_id: int):
    # 確認是否存在該關聯
    relation_exists = db.execute(
        text("SELECT 1 FROM has WHERE toilet_id = :toilet_id AND amenity_id = :amenity_id"),
        {"toilet_id": toilet_id, "amenity_id": amenity_id}
    ).fetchone()

    if not relation_exists:
        return None

    # 刪除關聯
    db.execute(
        text("DELETE FROM has WHERE toilet_id = :toilet_id AND amenity_id = :amenity_id"),
        {"toilet_id": toilet_id, "amenity_id": amenity_id}
    )
    db.commit()

    # 回傳該廁所最新資料
    row = db.execute(
        text("SELECT * FROM toilet WHERE id = :id"), {"id": toilet_id}
    ).fetchone()

    return dict(row._mapping) if row else None
