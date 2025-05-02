from pydantic import BaseModel, Field
from datetime import date as dt_date

class Expense(BaseModel):
    date: dt_date = Field(default_factory=lambda: dt_date(2025, 1, 1))
    category: str = Field(default="Null")
    price_ARS: float = Field(default=0.0)
    paymentMethod: str = Field(default="Efectivo ARS")