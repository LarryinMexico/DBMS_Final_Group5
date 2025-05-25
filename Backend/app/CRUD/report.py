from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import report as schemas

""""以下for user"""

# 創建報告
def create_report(db: Session, report: schemas.ReportCreate):
    """創建新報告"""
    insert_query = text("""
        INSERT INTO report (user_id, toilet_id, description, status) 
        VALUES (:user_id, :toilet_id, :description, :status)
    """)
    
    # 執行插入
    result = db.execute(insert_query, {
        "user_id": report.user_id,
        "toilet_id": report.toilet_id,
        "description": report.description,
        "status": "pending"  # 預設狀態
    })
    db.commit()
    
    # 取得插入記錄的 ID
    inserted_id = result.lastrowid
    
    # 查詢剛插入的記錄
    select_query = text("SELECT * FROM report WHERE id = :id")
    result = db.execute(select_query, {"id": inserted_id})
    row = result.fetchone()
    
    if row:
        return dict(row._mapping)
    return None

# user獲取自己的報告
def get_reports_by_user(db: Session, user_id: int):
    """根據用戶 ID 獲取報告"""
    query = text("SELECT * FROM report WHERE user_id = :user_id")
    result = db.execute(query, {"user_id": user_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

# 刪除報告
def delete_report(db: Session, report_id: int):
    """刪除報告"""
    # 先檢查記錄是否存在
    check_query = text("SELECT id FROM report WHERE id = :report_id")
    result = db.execute(check_query, {"report_id": report_id})
    existing = result.fetchone()
    
    if existing is None:
        return False
    
    # 執行刪除
    delete_query = text("DELETE FROM report WHERE id = :report_id")
    db.execute(delete_query, {"report_id": report_id})
    db.commit()
    
    return True

"""以下for admin"""

# 更新報告狀態
def update_report_status(db: Session, report_update: schemas.ReportUpdate):
    """更新報告狀態"""
    # 先檢查報告是否存在
    check_query = text("SELECT * FROM report WHERE id = :report_id")
    result = db.execute(check_query, {"report_id": report_update.id})
    existing_report = result.fetchone()
    
    if existing_report is None:
        return False
    
    # 檢查狀態值是否有效
    valid_statuses = ["pending", "resolved", "rejected"]
    if report_update.status not in valid_statuses:
        return False
    
    # 更新狀態
    update_query = text("UPDATE report SET status = :status WHERE id = :report_id")
    db.execute(update_query, {
        "status": report_update.status,
        "report_id": report_update.id
    })
    db.commit()
    
    # 查詢更新後的記錄
    result = db.execute(check_query, {"report_id": report_update.id})
    updated_row = result.fetchone()
    
    if updated_row:
        return dict(updated_row._mapping)
    return False

# 通過ID獲取報告
def get_report_by_id(db: Session, report_id: int):
    """根據 ID 獲取報告"""
    query = text("SELECT * FROM report WHERE id = :report_id")
    result = db.execute(query, {"report_id": report_id})
    row = result.fetchone()
    if row:
        return dict(row._mapping)
    return None

# 獲取所有報告
def get_all_reports(db: Session, skip: int = 0, limit: int = 100):
    """獲取所有報告（支援分頁）"""
    query = text("SELECT * FROM report LIMIT :limit OFFSET :skip")
    result = db.execute(query, {"limit": limit, "skip": skip})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

# 通過廁所ID獲取報告
def get_reports_by_toilet(db: Session, toilet_id: int):
    """根據廁所 ID 獲取報告"""
    query = text("SELECT * FROM report WHERE toilet_id = :toilet_id")
    result = db.execute(query, {"toilet_id": toilet_id})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]

# 通過狀態篩選報告
def get_reports_by_status(db: Session, status: str):
    """根據狀態篩選報告"""
    valid_statuses = ["pending", "resolved", "rejected"]
    if status not in valid_statuses:
        return []
    
    query = text("SELECT * FROM report WHERE status = :status")
    result = db.execute(query, {"status": status})
    rows = result.fetchall()
    return [dict(row._mapping) for row in rows]