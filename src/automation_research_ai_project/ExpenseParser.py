import re
import json
from typing import List
from automation_research_ai_project.models.expense import Expense

class ExpenseParser:
    def parse_expenses(self, raw_output: str) -> List[Expense]:
        try:
            # 🔧 Clean // comments and trailing commas
            cleaned = re.sub(r"//.*", "", raw_output)
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
                        print(f"⚠️  Field '{{key}}' was empty or invalid, default will be used.")
                        item[key] = None
                expenses.append(Expense(**item))

            return expenses

        except Exception as e:
            print("❌ Failed to parse LLM output:")
            print("🔎 Raw output:\\n", raw_output)
            raise e
