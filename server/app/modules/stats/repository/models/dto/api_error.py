from pydantic import BaseModel
from typing import Any
from datetime import datetime


class APIError(BaseModel):
    message: str
    time: datetime | None = None
    bug: str | None = None
    plan: str | None = None
    report: Any | None = None
