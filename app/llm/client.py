import json

from google import genai

from app.config.settings import settings


class GeminiClient:
    """Gemini API client."""

    def __init__(self) -> None:
        api_key = settings.gemini_api_key

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self._client = genai.Client(api_key=api_key)

        self._model = settings.gemini_model

    def generate_json(
        self,
        prompt: str,
    ) -> dict:
        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
        )

        return json.loads(response.text)
