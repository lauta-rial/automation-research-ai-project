from pydantic import BaseModel
from typing import List
from automation_research_ai_project.models.expense import Expense

class ExpenseList(BaseModel):
    expenses: List[Expense]