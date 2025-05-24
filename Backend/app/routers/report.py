from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.schemas import report as schemas
from app.CRUD import report as crud

router = APIRouter()

"""一般用戶"""

# 創建報告
@router.post("/", response_model=schemas.ReportListItem, status_code=status.HTTP_201_CREATED,summary="Create a new report")
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    return crud.create_report(db=db, report=report)

# user獲取自己的報告
@router.get("/user/{user_id}", response_model=List[schemas.ReportListItem],summary="Get reports by user ID")
def get_user_reports(user_id: int, db: Session = Depends(get_db)):
    reports = crud.get_reports_by_user(db=db, user_id=user_id)
    return reports

# 刪除報告
@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT,summary="Delete a report")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    success = crud.delete_report(db=db, report_id=report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return None

""""管理員"""

# 依report_id獲取特定報告
@router.get("/{report_id}", response_model=schemas.ReportListItem, summary="Get a report by ID (admin)")
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = crud.get_report_by_id(db=db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return db_report

# 更新報告狀態
@router.put("/{report_id}", response_model=schemas.ReportListItem, summary="Update report status (admin)")
def update_report(report_id: int, report_update: schemas.ReportUpdate, db: Session = Depends(get_db)):
    # 確保路徑參數與請求體中的ID一致
    if report_id != report_update.id:
        raise HTTPException(status_code=400, detail="Path ID does not match body ID")
    
    updated_report = crud.update_report_status(db=db, report_update=report_update)
    if not updated_report:
        raise HTTPException(status_code=404, detail="Report not found or invalid status")
    return updated_report

# 獲取所有報告
@router.get("/", response_model=List[schemas.ReportListItem], summary="Get all reports (admin)")
def read_reports(skip: int = 0, limit: int = 100, status: Optional[str] = None, db: Session = Depends(get_db)):
    if status:
        reports = crud.get_reports_by_status(db=db, status=status)
        if not reports and status not in ["pending", "resolved", "rejected"]:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: pending, resolved, rejected")
        return reports
    return crud.get_all_reports(db=db, skip=skip, limit=limit)

# 獲取特定廁所的所有報告
@router.get("/toilet/{toilet_id}", response_model=List[schemas.ReportListItem], summary="Get all reports for a specific toilet (admin)")
def get_toilet_reports(toilet_id: int, db: Session = Depends(get_db)):
    reports = crud.get_reports_by_toilet(db=db, toilet_id=toilet_id)
    return reports