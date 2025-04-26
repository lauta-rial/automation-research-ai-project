from pydantic import BaseModel
from typing import Optional
from datetime import date

class Expense(BaseModel):
    date: date
    category: str
    price_ARS: float
    price_USD: Optional[float] = None
    description: str
    paymentMethod: str