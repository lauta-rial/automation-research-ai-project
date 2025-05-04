from typing import List, Union
from automation_research_ai_project.models.expense import Expense
from automation_research_ai_project.prompts.PromptFormatter import PromptFormatter
from automation_research_ai_project.LLMClient import LLMClient
from automation_research_ai_project.ExpenseParser import ExpenseParser

class TextHandler:
    """
    This class is responsible for handling text files and extracting expense information.
    """
    def __init__(self, prompt_file: str, default_date: str, model_name: str):
        self.prompt_formatter = PromptFormatter(prompt_file, default_date)
        self.llm_client = LLMClient(model_name)
        self.expense_parser = ExpenseParser()

    def handle_text(self, file_path: str) -> Union[Expense, List[Expense]]:
        with open(file_path, 'r', encoding='utf-8') as f:
            user_input = f.read()

        fields = Expense.__annotations__.keys()
        fields_str = "\\n".join(f"- {field}" for field in fields)

        prompt = self.prompt_formatter.format_prompt(fields_str, user_input)
        raw_output = self.llm_client.chat(prompt)
        expenses = self.expense_parser.parse_expenses(raw_output)

        return expenses if len(expenses) > 1 else expenses[0]
