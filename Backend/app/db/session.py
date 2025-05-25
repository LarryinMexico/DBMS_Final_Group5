from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://test:@34.81.148.151:3306/toilet_dev"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,         # ✅ 提高常駐連線數
    max_overflow=20,      # ✅ 容許額外高峰使用
    pool_timeout=30,      # ✅ 最長等候秒數
    pool_recycle=1800,    # ✅ 每 30 分鐘重連（防止 MySQL 自動斷線）
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()