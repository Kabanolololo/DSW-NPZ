from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

# Schemat bazowy samochodu
class CarBase(BaseModel):
    brand: str = Field(..., example="Toyota")
    model: str = Field(..., example="Corolla")
    year: int = Field(..., example=2022)
    color: str = Field(..., example="Red")
    price_per_day: float = Field(..., example=100)
    availability: Optional[str] = Field(default="available", example="available")

# Schemat do tworzenia nowego samochodu
class CarCreate(CarBase):
    pass

# Schemat do aktualizacji samochodu
class CarUpdate(BaseModel):
    brand: Optional[str] = Field(None, example="Toyota")
    model: Optional[str] = Field(None, example="Corolla")
    year: Optional[int] = Field(None, example=2022)
    color: Optional[str] = Field(None, example="Red")
    price_per_day: Optional[float] = Field(None, example=100)
    availability: Optional[str] = Field(None, example="available")

# Schemat pełnego samochodu do odpowiedzi
class CarResponse(CarBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Schemat listy samochodów (jeśli potrzebny)
class CarListSchema(BaseModel):
    cars: List[CarResponse]
