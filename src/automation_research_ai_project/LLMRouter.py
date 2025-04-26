import os
import re
import json
import ollama
import textwrap
from typing import List
from automation_research_ai_project.models.expense import Expense

class LLMRouter:
    def __init__(self, base_folder: str):
        self.base_folder = base_folder
        self.handlers = {
            "text": self.handle_text,
            "audio": self.handle_audio,
            "img": self.handle_image,
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
                    results.append(expense)
                except Exception as e:
                    print(f"❌ Error processing {file_path}: {e}")
        return results

    def handle_text(self, file_path: str) -> Expense:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        fields = Expense.__annotations__.keys()
        fields_str = "\n".join(f"- {field}" for field in fields)

        prompt = textwrap.dedent(f"""
            You are an assistant that extracts structured expense data from user text.
            Respond ONLY with a valid JSON object. Do not include placeholders or explanations.
            Wrap all objects in square brackets. Do not forget the opening and closing [ ].
            Add 2024-10-13 to the date field. By default all prices are in ARS.
            paymentMethod field by default should be a string.
            description field by default should be a string.
            Please return a JSON object with the following fields ONLY:
            {fields_str}
            Text:
            \"\"\"
            {content}
            \"\"\"
        """)

        response = ollama.chat(
            model='mistral:latest',
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            raw = response['message']['content']

            # 🔧 Clean // comments and trailing commas
            cleaned = re.sub(r"//.*", "", raw)
            cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)

            # 🛠️ Wrap raw blocks in array if not already
            cleaned_stripped = cleaned.strip()
            if cleaned_stripped.startswith("{") and cleaned_stripped.count("}") > 1:
                cleaned = f"[{cleaned}]"

            parsed = json.loads(cleaned)

            # 🔁 Ensure list for consistent processing
            parsed_items = parsed if isinstance(parsed, list) else [parsed]

            # 🧾 Build Expense objects using Pydantic defaults
            expenses = []
            for item in parsed_items:
                # These fields can safely default to None (your Pydantic model will cover them)
                nullable_fields = {"date", "description", "paymentMethod", "price_USD"}

                for key, value in item.items():
                    if key in nullable_fields and (
                        value is None or (isinstance(value, str) and value.strip().lower() in {"", "none", "null", "not provided"})
                    ):
                        print(f"⚠️  Field '{key}' was empty or invalid, default will be used.")
                        item[key] = None
                expenses.append(Expense(**item))

            return expenses if len(expenses) > 1 else expenses[0]

        except Exception as e:
            print("❌ Failed to parse LLM output:")
            print("🔎 Raw output:\n", raw)
            raise e
    
    def handle_audio(self, file_path: str) -> Expense:
        # TODO: Add Whisper transcription and call LLM on transcript
        return self.handle_text(file_path)

    def handle_image(self, file_path: str) -> Expense:
        # TODO: Add OCR (e.g. pytesseract) and call LLM on extracted text
        return self.handle_text(file_path)
