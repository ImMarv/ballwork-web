"""Digest run repository module for exclusively adding digest runs."""

from datetime import datetime
from typing import Protocol

from sqlalchemy.orm import Session

from .models.digest_run_digest import DigestRun, DigestStatus


class DigestRunRepository(Protocol):
    """Class dealing with DOA for Digest Runs

    Args:
        Protocol (_type_): _description_

    Returns:
        _type_: _description_
    """

    session: Session

    def add_run(self, subscriber_id: int, period_start: datetime, status: str):
        run = DigestRun(
            subscriber_id=subscriber_id,
            period_start=period_start,
            status=status,
            sent_at=datetime.now(),
        )
        self.session.add(run)
        self.session.commit()
        return run
