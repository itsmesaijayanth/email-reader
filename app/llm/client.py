import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """Gemini API client."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self._client = genai.Client(api_key=api_key)

        self._model = os.getenv("GEMINI_MODEL")

    def generate_json(
        self,
        prompt: str,
    ) -> dict:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        return json.loads(response.text)
