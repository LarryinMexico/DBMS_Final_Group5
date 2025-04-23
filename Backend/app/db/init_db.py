from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.building import Building
from app.models.toilet import Toilet
from app.models.review import Review
# 💡 不 import User，就不會 drop 它！

def reset_db():
    # ⚠️ 只 drop & create building、toilet 這兩個表格
    Base.metadata.drop_all(bind=engine, tables=[Building.__table__, Toilet.__table__, Review.__table__,])
    Base.metadata.create_all(bind=engine, tables=[Building.__table__, Toilet.__table__, Review.__table__,])

if __name__ == "__main__":
    reset_db()
    print("Database reset complete.")

# cd Backend
# PYTHONPATH=. python3 app/db/init_db.py