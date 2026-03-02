"""Digest run repository module for exclusively adding digest runs."""

from typing import Protocol

from sqlalchemy.orm import Session

from .models.digest_run_digest import DigestRun


class DigestRunRepository(Protocol):
    """Class dealing with DOA for Digest Runs

    Args:
        Protocol (_type_): _description_

    Returns:
        _type_: _description_
    """

    session: Session

    def add_run(self, run: DigestRun):
        """Adds digest run to DB

        Args:
            run (DigestRun): Digest Run object
        """
        return self.session.add(run)
