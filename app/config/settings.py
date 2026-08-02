from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    gemini_api_key: str = Field(alias="GEMINI_API_KEY")

    gemini_model: str = Field(
        default="gemini-2.5-flash-lite",
        alias="GEMINI_MODEL",
    )

    gmail_max_results: int = Field(
        default=10,
        alias="GMAIL_MAX_RESULTS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
