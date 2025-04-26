from pydantic import BaseModel

# 創建報告
class ReportCreate(BaseModel):
    user_id: int
    toilet_id: int
    description: str

# 狀態更新
class ReportUpdate(BaseModel):
    id: int
    status: str  # 狀態可以是 "pending", "resolved", "rejected" 

# 顯示報告
class ReportList(BaseModel):
    id: int

# 刪除報告
class ReportList(BaseModel):
    id: int

