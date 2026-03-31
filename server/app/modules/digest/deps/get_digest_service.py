"""Digest service factory dependency."""

from app.db import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

from server.app.modules.digest.email.factory import build_email_service
from server.app.modules.digest.repository.digest_run_repo import SQLDigestRunRepository
from server.app.modules.digest.repository.event_repo import SQLEventRepository
from server.app.modules.digest.repository.subscriber_repo import SQLSubscriberRepository
from server.app.modules.digest.repository.subscription_repo import (
    SQLSubscriptionRepository,
)
from server.app.modules.digest.service import DigestService


def get_digest_service(db: Session = Depends(get_db)) -> DigestService:  # noqa: B008
    return DigestService(
        event_repo=SQLEventRepository(db),
        subscriber_repo=SQLSubscriberRepository(db),
        subscription_repo=SQLSubscriptionRepository(db),
        digest_run_repo=SQLDigestRunRepository(db),
        email_service=build_email_service(),
    )
