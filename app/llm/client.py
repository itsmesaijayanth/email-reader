import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiClient:
    """Thin wrapper around the Gemini API."""

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self._model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash-lite",
        )

        self._client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        """Generate text using Gemini."""

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        return response.text or ""
