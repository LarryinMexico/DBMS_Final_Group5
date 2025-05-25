from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import Favorite, Review, Reaction, Report, Toilet, Building, Amenity
from app.models.follow import Follow
from app.models.has import has

def clear_all_but_users():
    db: Session = SessionLocal()

    try:
        # 先刪掉關聯的子資料表
        db.query(Reaction).delete()
        db.query(Favorite).delete()
        db.query(Report).delete()
        db.query(Follow).delete()
        db.query(has).delete()

        # 再刪除與 user 有 FK 的父表
        db.query(Review).delete()

        # 接著刪除其他資源表
        db.query(Toilet).delete()
        db.query(Building).delete()
        db.query(Amenity).delete()

        db.commit()
        print("✅ 所有非使用者資料已清空")
    except Exception as e:
        db.rollback()
        print("❌ 清除資料失敗：", e)
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_but_users()