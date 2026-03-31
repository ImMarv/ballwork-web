"""Digest service factory dependency."""

from app.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from ..email.factory import build_email_service
from ..repository.digest_run_repo import SQLDigestRunRepository
from ..repository.event_repo import SQLEventRepository
from ..repository.subscriber_repo import SQLSubscriberRepository
from ..repository.subscription_repo import (
    SQLSubscriptionRepository,
)
from ..service import DigestService


def get_digest_service(db: Session = Depends(get_db)) -> DigestService:  # noqa: B008
    return DigestService(
        event_repo=SQLEventRepository(db),
        subscriber_repo=SQLSubscriberRepository(db),
        subscription_repo=SQLSubscriptionRepository(db),
        digest_run_repo=SQLDigestRunRepository(db),
        email_service=build_email_service(),
    )
