from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from schemas.car_schema import CarResponse, CarCreate, CarUpdate
from crud.cars_crud import get_all_cars, get_car_by_id, create_car, update_car, delete_car
from api.dependencies import get_db
from utils.jwt import get_current_user
from models.car import Car as CarModel

router = APIRouter()

################### Endpointy dla wszystkich użytkowników ###################

@router.get("/", response_model=List[CarResponse])
def read_all_cars(db: Session = Depends(get_db)):
    return get_all_cars(db)

@router.get("/{car_id}", response_model=CarResponse)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

################### Endpointy dla administratorów ###################

@router.post("/admin", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_new_car(
    car: CarCreate,
    token: str = Query(..., description="JWT token"),
    db: Session = Depends(get_db)
):
    current_user_data = get_current_user(token=token, db=db)

    if current_user_data.role != "admin":
        raise HTTPException(status_code=403, detail="Nie masz uprawnień do dodania samochodu.")

    new_car = CarModel(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return new_car

@router.put("/admin/{car_id}", response_model=CarResponse)
def update_existing_car(
    car_id: int,
    car: CarUpdate,
    token: str = Query(..., description="JWT token"),
    db: Session = Depends(get_db),
):
    current_user_data = get_current_user(token=token, db=db)

    if current_user_data.role != "admin":
        raise HTTPException(status_code=403, detail="Nie masz uprawnień do edycji.")

    updated_car = update_car(db, car_id, car)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated_car

@router.delete("/admin/{car_id}")
def delete_existing_car(
    car_id: int,
    token: str = Query(..., description="JWT token"),
    db: Session = Depends(get_db),
):
    current_user_data = get_current_user(token=token, db=db)

    if current_user_data.role != "admin":
        raise HTTPException(status_code=403, detail="Nie masz uprawnień do usuwania.")

    success = delete_car(db, car_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Samochód usunięty pomyślnie"}
