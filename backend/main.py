from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal, engine, Base
from models import car, reservation, review, user
#from api.items import router as items_router

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

#app.include_router(items_router, prefix="/items", tags=["grocery-items"])




