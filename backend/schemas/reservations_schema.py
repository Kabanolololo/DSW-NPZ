from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Bazowy schemat – wspólny dla create/response
class ReservationBase(BaseModel):
    user_id: int = Field(..., example=1)
    car_id: int = Field(..., example=2)
    start_date: datetime = Field(..., example="2025-06-01T10:00:00")
    end_date: datetime = Field(..., example="2025-06-05T10:00:00")

# Schemat do tworzenia nowej rezerwacji (żadne dodatkowe pola)
class ReservationCreate(ReservationBase):
    pass

# Schemat do aktualizacji (daty są opcjonalne)
class ReservationUpdate(BaseModel):
    start_date: Optional[datetime] = Field(None, example="2025-06-02T10:00:00")
    end_date: Optional[datetime] = Field(None, example="2025-06-06T10:00:00")

# Schemat odpowiedzi (zawiera ID, wymagany przez response_model)
class ReservationResponse(ReservationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
