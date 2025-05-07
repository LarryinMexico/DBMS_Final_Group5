from sqlalchemy.orm import Session
from app.models import report as models
from app.schemas import report as schemas

""""以下for user"""

# 創建報告
def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(
        user_id=report.user_id,
        toilet_id=report.toilet_id,
        description=report.description,
        status="pending"  # 預設狀態
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

# user獲取自己的報告
def get_reports_by_user(db: Session, user_id: int):
    return db.query(models.Report).filter(models.Report.user_id == user_id).all()

# 刪除報告
def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if report is None:
        return False
    db.delete(report)
    db.commit()
    return True

"""以下for admin"""

# 更新報告狀態
def update_report_status(db: Session, report_update: schemas.ReportUpdate):
    report = db.query(models.Report).filter(models.Report.id == report_update.id).first()
    if report is None:
        return False
    
    # 檢查狀態值是否有效
    valid_statuses = ["pending", "resolved", "rejected"]
    if report_update.status not in valid_statuses:
        return False
    
    report.status = report_update.status
    db.commit()
    db.refresh(report)
    return report

# 通過ID獲取報告
def get_report_by_id(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

# 獲取所有報告
def get_all_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Report).offset(skip).limit(limit).all()


# 通過廁所ID獲取報告
def get_reports_by_toilet(db: Session, toilet_id: int):
    return db.query(models.Report).filter(models.Report.toilet_id == toilet_id).all()

# 通過狀態篩選報告
def get_reports_by_status(db: Session, status: str):
    valid_statuses = ["pending", "resolved", "rejected"]
    if status not in valid_statuses:
        return []
    return db.query(models.Report).filter(models.Report.status == status).all()