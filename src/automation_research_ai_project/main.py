import os
import json
from automation_research_ai_project.LLMRouter import LLMRouter
from automation_research_ai_project.models.expense import Expense

def main():
    # 📂 Folder where text, audio, and img subfolders live
    base_folder = os.path.join(
        os.path.dirname(__file__), "interactions"
    )

    # ⚙️ Initialize and run router
    router = LLMRouter(base_folder)
    results = router.run()

    # 🔁 Ensure results is a flat list of Expense objects
    flat_expenses = []
    if isinstance(results, list):
        for item in results:
            if isinstance(item, list):
                flat_expenses.extend(item)
            else:
                flat_expenses.append(item)
    else:
        flat_expenses = [results]

    # 📋 Output formatted JSON
    print("\n📋 Processed Expenses:")
    for expense in flat_expenses:
        print(json.dumps(expense.model_dump(), indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()
