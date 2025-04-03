# 🚽 Toilet Map Backend

這是「政大廁所 Review Map」的後端專案，使用 FastAPI + MySQL 開發，部署在 GCP（Cloud Run + Cloud SQL）上。

## 📁 專案結構

```text
Backend/
├── Dockerfile
├── requirements.txt
├── app
│   ├── main.py               # FastAPI 啟動入口
│   ├── models                # SQLAlchemy Models（資料表定義）
│   │   └── user.py
│   ├── schemas               # Pydantic Schemas（請求與回傳格式）
│   │   └── user.py
│   ├── CRUD                  # 資料庫操作邏輯
│   │   └── user.py
│   ├── routers               # API 路由定義
│   │   └── user.py
│   ├── db
│   │   ├── base.py           # Base = declarative_base()
│   │   └── session.py        # engine 與 SessionLocal
```

## 🛠 建立新資料表 Entity 流程（以非 User 為主）

1. 在 `models/` 下新增資料表 Model：

```python
# app/models/toilet.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Toilet(Base):
    __tablename__ = "toilets"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(255), nullable=False)
    floor = Column(String(50))
    gender = Column(String(20))
```

2. 在 `schemas/` 下建立 schema：

```python
# app/schemas/toilet.py
from pydantic import BaseModel

class ToiletBase(BaseModel):
    location: str
    floor: str | None = None
    gender: str | None = None

class ToiletCreate(ToiletBase):
    pass

class ToiletOut(ToiletBase):
    id: int

    model_config = {"from_attributes": True}
```

3. 在 `CRUD/` 下新增操作邏輯：

```python
# app/CRUD/toilet.py
from sqlalchemy.orm import Session
from app.models import toilet as models
from app.schemas import toilet as schemas

def create_toilet(db: Session, toilet: schemas.ToiletCreate):
    db_toilet = models.Toilet(**toilet.dict())
    db.add(db_toilet)
    db.commit()
    db.refresh(db_toilet)
    return db_toilet

def get_all_toilets(db: Session):
    return db.query(models.Toilet).all()
```

4. 在 `routers/` 下建立路由：

```python
# app/routers/toilet.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.CRUD import toilet as crud
from app.schemas import toilet as schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ToiletOut)
def create_toilet(toilet: schemas.ToiletCreate, db: Session = Depends(get_db)):
    return crud.create_toilet(db, toilet)

@router.get("/", response_model=list[schemas.ToiletOut])
def list_toilets(db: Session = Depends(get_db)):
    return crud.get_all_toilets(db)
```

5. 記得在 `main.py` 中加入路由：

```python
from app.routers import toilet
app.include_router(toilet.router, prefix="/toilets", tags=["Toilets"])
```

---

接下來可以繼續設計其他資料表，例如 Review、Favorite、Comment 等，維持一致的模式開發即可 🧻✨
