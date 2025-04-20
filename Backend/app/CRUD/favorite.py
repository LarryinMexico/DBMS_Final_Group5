from sqlalchemy.orm import Session
from app.models import favorite as models
from app.schemas import favorite as schemas

def get_favorite_list(db: Session, UserID: int):
    return db.query(models.Favorite).filter(models.Favorite.UserID == UserID).all()

def add_toilet(db: Session, UserID: int, ToiletID: int):
    new_fav=models.Favorite(
        UserID = UserID,
        ToiletID = ToiletID
    )
    db.add(new_fav)
    db.commit()
    return "Toielet added sucessfully"

def del_toilet(db: Session, FavoriteID: int):
    del_fav=db.query(models.Favorite).filter(models.Favorite.FavoriteID == FavoriteID).first()
    db.delete(del_fav)
    db.commit()
    return "Toielet deleted sucessfully"
