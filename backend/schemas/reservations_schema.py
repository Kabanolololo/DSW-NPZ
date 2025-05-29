from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from schemas.car_schema import CarResponse

# Bazowy schemat – wspólny dla create/response
class ReservationBase(BaseModel):
    user_id: int = Field(..., example=1)
    car_id: int = Field(..., example=2)
    start_date: datetime = Field(..., example="2025-06-01T10:00:00")
    end_date: datetime = Field(..., example="2025-06-05T10:00:00")

# Schemat do tworzenia nowej rezerwacji
class ReservationCreate(ReservationBase):
    pass

# Schemat do aktualizacji (opcjonalne daty)
class ReservationUpdate(BaseModel):
    start_date: Optional[datetime] = Field(None, example="2025-06-02T10:00:00")
    end_date: Optional[datetime] = Field(None, example="2025-06-06T10:00:00")

# Schemat odpowiedzi (dodajemy obiekt car!)
class ReservationResponse(ReservationBase):
    id: int
    car: Optional[CarResponse]  # ⬅️ dzięki temu React może pokazać markę/model

    model_config = ConfigDict(from_attributes=True)
