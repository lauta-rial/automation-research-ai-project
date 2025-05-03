import os
import json
from dotenv import load_dotenv
from automation_research_ai_project.ExpenseExtractor import ExpenseExtractor
from automation_research_ai_project.models.expense import Expense
import csv

load_dotenv()

def main():
    base_folder = os.environ.get("BASE_FOLDER")
    output_csv = os.environ.get("OUTPUT_CSV")
    prompt_file = os.environ.get("PROMPT_FILE")
    default_date = os.environ.get("DEFAULT_DATE")
    model_name = os.environ.get("MODEL_NAME")

    # ⚙️ Initialize and run router
    expenseExtractor = ExpenseExtractor(base_folder, prompt_file, default_date, model_name)
    results = expenseExtractor.run()

    # 🔁 Ensure results is a flat list of Expense objects
    flat_expenses = []
    if isinstance(results, list):
        flat_expenses = results
    else:
        flat_expenses = [results]

    # 📋 Output formatted JSON
    print("\n📋 Processed Expenses:")
    for expense in flat_expenses:
        print(json.dumps(expense.model_dump(), indent=2, ensure_ascii=False, default=str))

    # 📁 Write to CSV file
    if flat_expenses:
        with open(output_csv, mode="w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=flat_expenses[0].model_dump().keys())
            writer.writeheader()
            for expense in flat_expenses:
                writer.writerow(expense.model_dump())

        print(f"\n✅ CSV exported to: {output_csv}")
    else:
        print("\n⚠️ No expenses to export to CSV.")

if __name__ == "__main__":
    main()
