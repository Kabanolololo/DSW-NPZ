from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime

from schemas.reservations_schema import ReservationCreate, ReservationResponse
from crud.reservations_crud import (
    create_reservation,
    cancel_reservation,
    get_available_dates,
    get_occupied_dates,
    delete_reservation,
)
from api.dependencies import get_db
from utils.jwt import get_current_user
from models.user import User
from models.reservation import Reservation

router = APIRouter()

def fix_date_format(dt_str):
    if dt_str and isinstance(dt_str, str):
        if dt_str.endswith("+02"):
            dt_str = dt_str + ":00"
        return datetime.fromisoformat(dt_str)
    return dt_str

################### Endpointy dla wszystkich użytkowników ###################

@router.get("/available-dates", response_model=List[str])
def available_dates(car_id: int, db: Session = Depends(get_db)):
    return get_available_dates(db, car_id)

################### Endpointy dla użytkowników zalogowanych ###################

@router.post("/", response_model=ReservationResponse)
def make_reservation(
    user_id: int,
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_role = current_user.role
    current_user_email = current_user.email

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_role != "admin" and current_user_email != db_user.email:
        raise HTTPException(status_code=403, detail="You do not have permission to do that")

    if reservation.user_id != user_id:
        raise HTTPException(status_code=400, detail="user_id in body must match user_id in URL")

    created_reservation = create_reservation(db, reservation)
    if created_reservation:
        created_reservation.start_date = fix_date_format(created_reservation.start_date)
        created_reservation.end_date = fix_date_format(created_reservation.end_date)
    else:
        raise HTTPException(status_code=400, detail="Reservation could not be created")

    return created_reservation

@router.delete("/{reservation_id}", response_model=dict)
def cancel_reservation_endpoint(
    user_id: int,
    reservation_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    current_user = get_current_user(token, db)
    current_role = current_user.role
    current_user_email = current_user.email

    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_role != "admin" and current_user_email != db_user.email:
        raise HTTPException(status_code=403, detail="You do not have permission to do that")

    success = cancel_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": "Reservation canceled successfully"}

################### Endpointy dla administratorów ###################

@router.get("/admin/occupied-dates", response_model=List[str])
def occupied_dates(
    car_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    current_user = get_current_user(token, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions.")

    return get_occupied_dates(db, car_id)

@router.delete("/admin/{reservation_id}")
def delete_reservation_endpoint(
    reservation_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    current_user = get_current_user(token, db)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions.")

    reservation = delete_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    return {"detail": f"Reservation {reservation_id} has been deleted successfully."}

################### NOWY ENDPOINT: /me ###################

@router.get("/me", response_model=List[ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    current_user = get_current_user(token, db)

    reservations = db.query(Reservation)\
        .options(joinedload(Reservation.car))\
        .filter(Reservation.user_id == current_user.id)\
        .all()

    return reservations


    # Pobierz rezerwacje razem z obiektami car (żeby były dostępne car.brand, car.model itd.)
    reservations = db.query(Reservation)\
        .options(joinedload(Reservation.car))\
        .filter(Reservation.user_id == current_user.id)\
        .all()

    return reservations
