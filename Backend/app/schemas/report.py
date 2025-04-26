from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional

# 創建報告
class ReportCreate(BaseModel):
    user_id: int
    toilet_id: int
    description: str

# 狀態更新
class ReportUpdate(BaseModel):
    id: int
    status: str  # 狀態可以是 "pending", "resolved", "rejected" 

# 顯示報告列表項目
class ReportListItem(BaseModel):
    id: int
    toilet_id: int
    status: str
    description: str
    
    class Config:
        orm_mode = True  # 允許從ORM對象讀取

# 刪除報告請求
class ReportDelete(BaseModel):
    id: int

