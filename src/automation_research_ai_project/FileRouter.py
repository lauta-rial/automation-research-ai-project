from typing import List
import os
from automation_research_ai_project.handlers.TextHandler import TextHandler
from automation_research_ai_project.handlers.AudioHandler import AudioHandler
from automation_research_ai_project.handlers.ImageHandler import ImageHandler
from automation_research_ai_project.models.expense import Expense

class FileRouter:
    def __init__(self, base_folder: str, text_handler: TextHandler, audio_handler: AudioHandler, image_handler: ImageHandler):
        self.base_folder = base_folder
        self.handlers = {
            "text": text_handler.handle_text,
            "audio": audio_handler.handle_audio,
            "img": image_handler.handle_image,
        }

    def run(self) -> List[Expense]:
        results = []
        input_folder = os.environ.get("INPUT_FOLDER", "src/automation_research_ai_project/input_folder")
        for category in os.listdir(input_folder):
            category_path = os.path.join(input_folder, category)
            if not os.path.isdir(category_path):
                continue
            handler = self.handlers.get(category)
            if not handler:
                print(f"❌ No handler for category {category}")
                continue
            for filename in os.listdir(category_path):
                file_path = os.path.join(category_path, filename)
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
