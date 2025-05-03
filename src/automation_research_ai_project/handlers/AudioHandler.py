from typing import List, Union
from automation_research_ai_project.models.expense import Expense

class AudioHandler:
    def handle_audio(self, file_path: str) -> Union[Expense, List[Expense]]:
        # TODO: Add Whisper transcription and call LLM on transcript
        # For now, return None
        return None
