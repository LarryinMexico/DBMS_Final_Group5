from sqlalchemy.orm import Session
from app.models import favorite as models
from app.schemas import favorite as schemas

def get_favorite_list(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def add_toilet(db: Session, input_user_id: int, input_toilet_id: int):
    new_fav=models.Favorite(
        user_id = input_user_id,
        toilet_id = input_toilet_id
    )
    db.add(new_fav)
    db.commit()
    return "Toilet added sucessfully"

def del_toilet(db: Session, user_id: int, toilet_id: int):
    fav = db.query(models.Favorite).filter_by(user_id=user_id, toilet_id=toilet_id).first()
    if not fav:
        return False
    db.delete(fav)
    db.commit()
    return True

