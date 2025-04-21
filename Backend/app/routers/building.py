from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.CRUD import building as crud
from app.schemas import building as schemas

router = APIRouter()

@router.get("/{building_id}", response_model=schemas.Building)
def read_building(building_id: int, db: Session = Depends(get_db)):
    db_building = crud.get_building(db, building_id=building_id)
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return db_building

@router.get("/", response_model=List[schemas.Building])
def read_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buildings = crud.get_buildings(db, skip=skip, limit=limit)
    return buildings

@router.post("/", response_model=schemas.Building)
def create_building(building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    return crud.create_building(db=db, building=building)

@router.put("/{building_id}", response_model=schemas.Building)
def update_building(building_id: int, building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    db_building = crud.update_building(db, building_id=building_id, building=building)
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return db_building

@router.delete("/{building_id}")
def delete_building(building_id: int, db: Session = Depends(get_db)):
    success = crud.delete_building(db, building_id=building_id)
    if not success:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building deleted successfully"} 