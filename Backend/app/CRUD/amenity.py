from sqlalchemy.orm import Session
from app.models.amenity import Amenity
from app.models.toilet import Toilet
from app.schemas import amenity as schemas

def get_amenity(db: Session, amenity_id: int):
    return db.query(Amenity).filter(Amenity.id == amenity_id).first()

def get_amenities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Amenity).offset(skip).limit(limit).all()

def create_amenity(db: Session, amenity: schemas.AmenityCreate):
    db_amenity = Amenity(**amenity.dict())
    db.add(db_amenity)
    db.commit()
    db.refresh(db_amenity)
    return db_amenity

def delete_amenity(db: Session, amenity_id: int):
    db_amenity = get_amenity(db, amenity_id)
    if db_amenity:
        db.delete(db_amenity)
        db.commit()
        return True
    return False


def add_amenity_to_toilet(db: Session, toilet_id: int, amenity_id: int):
    toilet = db.query(Toilet).filter(Toilet.id == toilet_id).first()
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity:
        toilet.amenities.append(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None

def remove_amenity_from_toilet(db: Session, toilet_id: int, amenity_id: int):
    toilet = db.query(Toilet).filter(Toilet.id == toilet_id).first()
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity and amenity in toilet.amenities:
        toilet.amenities.remove(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None