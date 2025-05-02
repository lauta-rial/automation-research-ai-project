import os
from typing import List
from automation_research_ai_project.TextHandler import TextHandler
from automation_research_ai_project.AudioHandler import AudioHandler
from automation_research_ai_project.ImageHandler import ImageHandler
from automation_research_ai_project.models.expense import Expense

class InputRouter:
    def __init__(self, base_folder: str, text_handler: TextHandler, audio_handler: AudioHandler, image_handler: ImageHandler):
        self.base_folder = base_folder
        self.handlers = {
            "text": text_handler.handle_text,
            "audio": audio_handler.handle_audio,
            "img": image_handler.handle_image,
        }

    def run(self) -> List[Expense]:
        results = []
        for category, handler in self.handlers.items():
            folder_path = os.path.join(self.base_folder, category)
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                print(f"🔄 Processing {file_path}...")
                try:
                    expense = handler(file_path)
                    if isinstance(expense, list):
                        results.extend(expense)
                    else:
                        results.append(expense)
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")
        return results
