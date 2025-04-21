from sqlalchemy.orm import Session
from app.models import Building as models
from app.schemas import building as schemas

def get_building(db: Session, building_id: int):
    return db.query(models.Building).filter(models.Building.building_id == building_id).first()

def get_buildings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Building).offset(skip).limit(limit).all()

def create_building(db: Session, building: schemas.BuildingCreate):
    db_building = models.Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

def update_building(db: Session, building_id: int, building: schemas.BuildingCreate):
    db_building = get_building(db, building_id)
    if not db_building:
        return None
    
    for key, value in building.dict().items():
        setattr(db_building, key, value)
    
    db.commit()
    db.refresh(db_building)
    return db_building

def delete_building(db: Session, building_id: int):
    db_building = get_building(db, building_id)
    if db_building:
        db.delete(db_building)
        db.commit()
        return True
    return False 