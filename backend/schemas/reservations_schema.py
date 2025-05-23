from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Schemat bazowy rezerwacji – używany jako podstawa do tworzenia i odczytu danych
class ReservationBase(BaseModel):
    user_id: int = Field(..., example=1)
    car_id: int = Field(..., example=2)
    start_date: datetime = Field(..., example="2025-06-01T10:00:00")
    end_date: datetime = Field(..., example="2025-06-05T10:00:00")

# Schemat do tworzenia nowej rezerwacji
class ReservationCreate(ReservationBase):
    pass

# Schemat do aktualizacji rezerwacji (daty są opcjonalne)
class ReservationUpdate(BaseModel):
    start_date: Optional[datetime] = Field(None, example="2025-06-02T10:00:00")
    end_date: Optional[datetime] = Field(None, example="2025-06-06T10:00:00")

# Schemat zwracany w odpowiedziach API – zawiera pełne dane rezerwacji wraz z ID i statusem
class Reservation(ReservationBase):
    id: int

    class Config:
        orm_mode = True
