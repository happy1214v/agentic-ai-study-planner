import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLM:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate(self, prompt):
        if not self.client:
            return "LLM is not configured yet. Please add OPENAI_API_KEY."

        try:
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=prompt,
            )

            return response.output_text

        except Exception as e:
            return f"LLM error: {str(e)}"