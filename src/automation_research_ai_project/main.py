import os
import json
from dotenv import load_dotenv
from automation_research_ai_project.ExpenseExtractor import ExpenseExtractor
from automation_research_ai_project.utils.csv_writer import write_csv

load_dotenv()

def main():
    base_folder = os.environ.get("BASE_FOLDER")
    output_csv = os.environ.get("OUTPUT_CSV")
    prompt_file = os.environ.get("PROMPT_FILE")
    default_date = os.environ.get("DEFAULT_DATE")
    model_name = os.environ.get("MODEL_NAME")

    # ⚙️ Initialize and run router
    expenseExtractor = ExpenseExtractor(base_folder, prompt_file, default_date, model_name)
    expenses = expenseExtractor.run()

    # 📋 Output formatted JSON
    print("\n📋 Processed Expenses:")
    for expense in expenses:
        print(json.dumps(expense.model_dump(), indent=2, ensure_ascii=False, default=str))

    # 📁 Write to CSV file
    if expenses:
        write_csv(output_csv, [expense.model_dump() for expense in expenses])

if __name__ == "__main__":
    main()
