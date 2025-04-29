from sqlalchemy.orm import Session
from app.models import toilet as models
from app.schemas import toilet as schemas

def get_toilet_by_id(db: Session, toilet_id: int):
    return db.query(models.Toilet).filter(models.Toilet.id == toilet_id).first()

def get_toilets_by_building_id(db: Session, building_id: int):
    return db.query(models.Toilet).filter(models.Toilet.building_id == building_id).all()

def get_toilets_by_floor(db: Session, building_id: int, floor: int):
    return db.query(models.Toilet).filter(
        models.Toilet.building_id == building_id,
        models.Toilet.floor == floor
    ).all()

def get_all_toilets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Toilet).offset(skip).limit(limit).all()

def create_toilet(db: Session, toilet: schemas.ToiletCreate):
    db_toilet = models.Toilet(**toilet.dict())
    db.add(db_toilet)
    db.commit()
    db.refresh(db_toilet)
    return db_toilet

def update_toilet(db: Session, toilet_id: int, toilet: schemas.ToiletUpdate):
    db_toilet = get_toilet_by_id(db, toilet_id)
    if not db_toilet:
        return None
    
    update_data = toilet.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_toilet, key, value)
    
    db.commit()
    db.refresh(db_toilet)
    return db_toilet

def delete_toilet(db: Session, toilet_id: int):
    db_toilet = get_toilet_by_id(db, toilet_id)
    if db_toilet:
        db.delete(db_toilet)
        db.commit()
        return True
    return False

def add_amenity_to_toilet(db: Session, toilet_id: int, amenity_id: int):
    from app.models.amenity import Amenity
    toilet = get_toilet_by_id(db, toilet_id)
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity:
        toilet.amenities.append(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None

def remove_amenity_from_toilet(db: Session, toilet_id: int, amenity_id: int):
    from app.models.amenity import Amenity
    toilet = get_toilet_by_id(db, toilet_id)
    amenity = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if toilet and amenity and amenity in toilet.amenities:
        toilet.amenities.remove(amenity)
        db.commit()
        db.refresh(toilet)
        return toilet
    return None