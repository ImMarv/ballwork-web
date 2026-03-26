"""Settings for Environmental Variables"""

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_FOOTBALL_KEY: str = Field(...)
    DATABASE_URL: str = Field(...)
    EMAIL_HOST: str = Field(default="localhost")
    EMAIL_PORT: int = Field(default=1025)
    EMAIL_USER: str | None = Field(default=None)
    EMAIL_PASSWORD: str | None = Field(default=None)
    EMAIL_FROM: str = Field(default="noreply@ballwork.dev")
    EMAIL_USE_TLS: bool = Field(default=False)

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


if TYPE_CHECKING:
    # For Pylance / type checkers only
    settings: Settings
else:
    # Runtime initialization
    settings = Settings()
