from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.review import Review
from models.user import User
from models.car import Car
from schemas.review_schema import ReviewCreate

# Dodaj nową recenzję
def create_rating(db: Session, review: ReviewCreate):
    car = db.query(Car).filter(Car.id == review.car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    user = db.query(User).filter(User.id == review.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_review = db.query(Review).filter(
        Review.user_id == review.user_id,
        Review.car_id == review.car_id
    ).first()

    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="User has already submitted a review for this car"
        )

    new_review = Review(**review.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# Pobierz wszystkie recenzje
def get_all_reviews(db: Session):
    return db.query(Review).all()

# Pobierz wszystkie recenzje dla danego samochodu
def get_reviews_by_car_id(db: Session, car_id: int):
    return db.query(Review).filter(Review.car_id == car_id).all()

# Usuń recenzję – tylko jeśli należy do użytkownika
def delete_rating(db: Session, rating_id: int, user_id: int):
    review = db.query(Review).filter(Review.id == rating_id, Review.user_id == user_id).first()
    if not review:
        return None
    db.delete(review)
    db.commit()
    return review

# Usuń recenzję – jako admin
def delete_rating_admin(db: Session, rating_id: int):
    review = db.query(Review).filter(Review.id == rating_id).first()
    if not review:
        return None
    db.delete(review)
    db.commit()
    return review
