from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List
from sqlalchemy.orm import Session
from schemas.review_schema import Review, ReviewCreate
from crud.review_crud import get_reviews_by_car_id,create_rating,delete_rating,delete_rating_admin,get_all_reviews
from models import User
from api.dependencies import get_db
from utils.jwt import get_current_user

router = APIRouter()

################### Endpointy dla wszystkich użytkowników ###################

# Endpoint do wyświetlenia wszystkich opinii dla konkretnego samochodu
@router.get("/{car_id}", response_model=List[Review])
def list_reviews_for_car(car_id: int, db: Session = Depends(get_db)):
    return get_reviews_by_car_id(db, car_id)

################### Endpointy dla użytkowników zalgowanych (logged-in users) ###################

# Endpoint do dodania opinii
@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def add_rating(
    user_id: int,
    rating: ReviewCreate,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    # Weryfikacja tokenu i uzyskanie danych użytkownika
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    current_user_email = current_user_data.get("email")

    # Sprawdzamy, czy użytkownik próbuje dodać recenzję jako sam siebie, jeśli nie jest adminem
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_role != "admin" and current_user_email != db_user.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to do that"
        )

    # Weryfikacja zgodności user_id w ciele i URL
    if rating.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id in body must match user_id in URL"
        )

    new_review = create_rating(db, rating)
    return new_review

# Endpoint do usunięcia opinii
@router.delete("/{rating_id}/user/{user_id}", response_model=Review)
def remove_rating(
    rating_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
    ):
    
    # Weryfikacja tokenu i uzyskanie danych użytkownika
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    current_user_email = current_user_data.get("email")

    # Sprawdzamy, czy użytkownik próbuje zaktualizować swoje dane
    if current_role != "admin" and current_user_email != db.query(User).filter(User.id == user_id).first().email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to do that"
        )
        
    rating = delete_rating(db, rating_id, user_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    

    return rating

################### Endpointy dla administratorów ###################

# Endpoint do wyświetlenia wszystkich opinii
@router.get("/admin/", response_model=List[Review])
def list_all_reviews(
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
        
    return get_all_reviews(db)

# Endpoint do usuniecia opinii
@router.delete("/admin/{rating_id}", status_code=200)
def delete_rating_endpoint(
    rating_id: int, 
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
        
    rating = delete_rating_admin(db, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"detail": f"Rating {rating_id} has been deleted successfully."}