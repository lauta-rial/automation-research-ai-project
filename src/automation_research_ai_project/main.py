import os
import json
from automation_research_ai_project.LLMRouter import LLMRouter
from automation_research_ai_project.models.expense import Expense

def main():
    # Base folder pointing to /interactions (where text, audio, img are)
    base_folder = os.path.join(
        os.path.dirname(__file__), "interactions"
    )

    # Init and run router
    router = LLMRouter(base_folder)
    expenses = router.run()

    # Output results
    print("\n📋 Processed Expenses:")
    for expense in expenses:
        print(json.dumps(expense.model_dump(), indent=2, ensure_ascii=False, default=str))

if __name__ == "__main__":
    main()
