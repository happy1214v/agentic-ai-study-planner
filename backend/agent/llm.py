import os
from dotenv import load_dotenv

load_dotenv()


class LLM:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate(self, prompt):
        if not self.api_key:
            return "LLM is not configured yet. Please add OPENAI_API_KEY."

        return "LLM API is ready."