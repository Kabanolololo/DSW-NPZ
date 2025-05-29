from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# URL do bazy danych PostgreSQL (możesz zmienić na inne, np. SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Disney2002.@localhost:5432/rental_cars")

# Tworzenie silnika połączenia z bazą danych
engine = create_engine(DATABASE_URL)

# Tworzenie sesji
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazowy model dla SQLAlchemy
Base = declarative_base()

# Funkcja pomocnicza do pobierania sesji DB dla FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
