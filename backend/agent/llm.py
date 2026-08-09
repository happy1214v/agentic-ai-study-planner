import os

import requests
from dotenv import load_dotenv


load_dotenv()


class LLM:
    def __init__(self):
        self.ollama_url = os.getenv(
            "OLLAMA_URL",
            "http://127.0.0.1:11434/api/generate",
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "llama3.2:3b",
        )

    def generate(self, prompt):
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "Ollama returned an empty response.",
            )

        except requests.exceptions.RequestException as e:
            return f"LLM error: {str(e)}"

        except Exception as e:
            return f"LLM error: {str(e)}"