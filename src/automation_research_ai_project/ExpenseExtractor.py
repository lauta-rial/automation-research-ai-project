import os
from typing import List
from automation_research_ai_project.FileRouter import FileRouter
from automation_research_ai_project.handlers.TextHandler import TextHandler
from automation_research_ai_project.handlers.AudioHandler import AudioHandler
from automation_research_ai_project.handlers.ImageHandler import ImageHandler
from automation_research_ai_project.models.expense import Expense

class ExpenseExtractor:
    """
    This class is responsible for extracting expenses from various file types.
    """
    def __init__(self, base_folder: str, prompt_file: str = os.environ.get("PROMPT_FILE"), default_date: str = os.environ.get("DEFAULT_DATE"), model_name: str = os.environ.get("MODEL_NAME")):
        self.base_folder = base_folder
        text_handler = TextHandler(prompt_file, default_date, model_name)
        audio_handler = AudioHandler()
        image_handler = ImageHandler()
        self.file_router = FileRouter(base_folder, text_handler, audio_handler, image_handler)

    def run(self) -> List[Expense]:
        results = self.file_router.run()

        # 🔁 Ensure results is a flat list of Expense objects
        flat_expenses = []
        if isinstance(results, list):
            flat_expenses = results
        else:
            flat_expenses = [results]

        return flat_expenses
