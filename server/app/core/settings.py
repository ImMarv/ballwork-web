"""Settings for Environmental Variables"""

from typing import TYPE_CHECKING

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_FOOTBALL_KEY: str = Field(...)

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
