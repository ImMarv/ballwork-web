from pydantic import BaseModel
from typing import Any


class APIError(BaseModel):
    message: str
    code: str | None = None
    field: str | None = None
    raw: Any | None = None
