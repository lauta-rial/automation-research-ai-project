from typing import List, Union
from automation_research_ai_project.models.expense import Expense

class ImageHandler:
    def handle_image(self, file_path: str) -> Union[Expense, List[Expense]]:
        # TODO: Add OCR (e.g. pytesseract) and call LLM on extracted text
        # For now, return None
        return None
