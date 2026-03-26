"""Settings for Environmental Variables"""

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ## Environments
    ENV: str = Field(default="dev", description="Environment to run in (e.g. dev, test, prod)")
    ## Required settings
    API_FOOTBALL_KEY: str = Field(...)
    DATABASE_URL: str = Field(...)
    RUN_SCHEDULER: bool = Field(default=True, description="Whether to run the scheduler")

    # Optional email settings
    EMAIL_HOST: str | None = Field(default=None, description="SMTP server host")
    EMAIL_PORT: int = Field(default=1025, description="SMTP server port")
    EMAIL_USER: str | None = Field(default=None, description="SMTP server username")
    EMAIL_PASSWORD: str | None = Field(default=None, description="SMTP server password")
    EMAIL_TEST: str | None = Field(default="test@ballwork.dev", description="Test email address to send digests to")

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
