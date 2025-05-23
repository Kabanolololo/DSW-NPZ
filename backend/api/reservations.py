from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.reservations_schema import Reservation, ReservationCreate
from crud.reservations_crud import create_reservation,cancel_reservation,get_available_dates,get_occupied_dates,delete_reservation
from api.dependencies import get_db
from utils.jwt import get_current_user
from models import User

router = APIRouter()

def fix_date_format(dt_str):
    if dt_str and isinstance(dt_str, str):
        if dt_str.endswith("+02"):
            dt_str = dt_str + ":00"
        return datetime.fromisoformat(dt_str)
    return dt_str

################### Endpointy dla wszystkich użytkowników ###################

# Endpoint do pobierania dostępnych dat dla danego samochodu
@router.get("/available-dates", response_model=List[str])
def available_dates(car_id: int, db: Session = Depends(get_db)):
    return get_available_dates(db, car_id)

################### Endpointy dla użytkowników zalgowanych (logged-in users) ###################

# Endpoint do tworzenia nowej rezerwacji
@router.post("/", response_model=Reservation)
def make_reservation(
    user_id: int,
    reservation: ReservationCreate, 
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
    ):
    
    # Weryfikacja tokenu i uzyskanie danych użytkownika
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    current_user_email = current_user_data.get("email")

    # Sprawdzamy, czy użytkownik próbuje dodać rezerwacje jako sam siebie, jeśli nie jest adminem
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_role != "admin" and current_user_email != db_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to do that"
        )    
        
    # Weryfikacja zgodności user_id w ciele i URL
    if reservation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id in body must match user_id in URL"
        )
        
    created_reservation = create_reservation(db, reservation)
    if created_reservation:
        created_reservation.start_date = fix_date_format(created_reservation.start_date)
        created_reservation.end_date = fix_date_format(created_reservation.end_date)
    else:
        raise HTTPException(status_code=400, detail="Reservation could not be created")
    return created_reservation

# Endpoint do anulowania rezerwacji
@router.delete("/{reservation_id}", response_model=dict)
def cancel_reservation_endpoint(
    user_id: int,
    reservation_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
    ):
    
    # Weryfikacja tokenu i uzyskanie danych użytkownika
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    current_user_email = current_user_data.get("email")
    
    # Sprawdzamy, czy użytkownik próbuje anulowac rezerwacje jako sam siebie, jeśli nie jest adminem
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_role != "admin" and current_user_email != db_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to do that"
        )    
        
    success = cancel_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": "Reservation canceled successfully"}

################### Endpointy dla administratorów ###################

# Endpoint do pobierania zajętych dat dla danego samochodu
@router.get("/admin/occupied-dates", response_model=List[str])
def occupied_dates(
    car_id: int, 
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
    ):
    
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")

    if current_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions."
        )
    return get_occupied_dates(db, car_id)

# Endpoint do usunięcia rezerwacji
@router.delete("/admin/{reservation_id}")
def delete_reservation_endpoint(
    reservation_id:
    int, 
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
    ):
    
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")

    if current_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions."
        )
        
    reservation = delete_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": f"Reservation {reservation_id} has been deleted successfully."}