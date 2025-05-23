from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, engine, Base
from models import car, reservation, review, user
from fastapi.middleware.cors import CORSMiddleware
from api.users import router as users_router
from api.auth import router as auth_router
from api.cars import router as cars_router
from api.reviews import router as review_router
from api.reservations import router as reservations_router

# Tworzymy tabele w bazie danych
Base.metadata.create_all(bind=engine)

# Tworzymy aplikację FastAPI
app = FastAPI(
    title="Luxury Car Rental API",
    description="A REST API for managing a luxury car rental service, created as part of a student term project.",
    version="1.0.0",
    contact={
        "name": "University Course Staff",
        "email": "support@example.edu"
    }
)

# Dodajemy middleware CORS
origins = [
    "http://localhost:8081",  
    "http://127.0.0.1:8081",
    "http://localhost:8080",
    "http://127.0.01:8080"
    #,"192.168.0.12" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["user"])
app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(review_router, prefix="/review", tags=["review"])
app.include_router(reservations_router, prefix="/reservations", tags=["reservations"])