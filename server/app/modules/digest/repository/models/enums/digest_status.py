from sqlalchemy import Enum


class DigestStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
