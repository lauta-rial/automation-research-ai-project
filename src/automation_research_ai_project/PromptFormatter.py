import textwrap

class PromptFormatter:
    def __init__(self, prompt_file: str, default_date: str):
        self.prompt_file = prompt_file
        self.default_date = default_date

    def format_prompt(self, fields_str: str, user_input: str) -> str:
        with open(self.prompt_file, 'r', encoding='utf-8') as f:
            prompt_template = f.read()

        prompt = textwrap.dedent(prompt_template).format(
            fields_str=fields_str,
            user_input=user_input,
            default_date=self.default_date
        )
        return prompt
