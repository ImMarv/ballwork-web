"""Settings for Environmental Variables"""

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ## Environments
    ENV: str = Field(
        default="dev", description="Environment to run in (e.g. dev, test, prod)"
    )
    ## Required settings
    API_FOOTBALL_KEY: str = Field(default="")
    STATS_PROVIDER: str = Field(default="api_football")
    MOCK_STATS_LATENCY_MIN_MS: int = Field(default=60)
    MOCK_STATS_LATENCY_MAX_MS: int = Field(default=220)
    MOCK_API_BASE_URL: str = Field(default="http://localhost:8081")
    DATABASE_URL: str = Field(...)
    EMAIL_HOST: str = Field(default="localhost")
    EMAIL_PORT: int = Field(default=1025)
    EMAIL_USER: str | None = Field(default=None)
    EMAIL_PASSWORD: str | None = Field(default=None)
    EMAIL_FROM: str = Field(default="noreply@ballwork.dev")
    EMAIL_USE_TLS: bool = Field(default=False)

    model_config = {
        "env_file": ".env.local",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


if TYPE_CHECKING:
    # For Pylance / type checkers only
    settings: Settings
else:
    # Runtime initialization
    settings = Settings()
