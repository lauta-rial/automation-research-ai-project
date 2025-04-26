from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as dt_date

class Expense(BaseModel):
    date: dt_date = Field(default_factory=lambda: dt_date(2025, 1, 1))
    category: str = Field(default="Other")
    price_ARS: Optional[float] = Field(default=None)
    price_USD: Optional[float] = Field(default=None)
    description: str = Field(default="Sin descripción")
    paymentMethod: str = Field(default="Efectivo ARS")