"""Thin API layer for digest module."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from .deps.get_digest_service import get_digest_service
from .repository.models.subscription import Subscription
from .service import DigestService

router = APIRouter()


class SubscriberCreateRequest(BaseModel):
    email: EmailStr


class SubscriberDeleteRequest(BaseModel):
    subscriber_id: int


class SubscriptionCreateRequest(BaseModel):
    subscriber_id: int
    entity_id: int
    entity_type: str
    target_type: str
    email: EmailStr | None = None


class SubscriptionDeleteRequest(BaseModel):
    subscription_id: int


@router.post("/digest/subscriber")
def create_subscriber(
    payload: SubscriberCreateRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    digest.subscriber_repo.create(payload.email)
    return {
        "status": "success",
        "message": f"{payload.email} subscribed to the digest.",
    }


@router.post("/digest/unsubscribe")
def delete_subscriber(
    payload: SubscriberDeleteRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    deleted = digest.subscriber_repo.delete(payload.subscriber_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Subscriber with ID {payload.subscriber_id} not found.",
        )

    return {
        "status": "success",
        "message": (
            f"Subscriber with ID {payload.subscriber_id} unsubscribed "
            "from the digest."
        ),
    }


@router.post("/digest/subscription/add")
def create_subscription(
    payload: SubscriptionCreateRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    subscriber = digest.subscriber_repo.get_by_id(payload.subscriber_id)

    if subscriber is None:
        if payload.email is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Subscriber with ID {payload.subscriber_id} not found. "
                    "Create the subscriber first or provide an email."
                ),
            )

        subscriber = digest.subscriber_repo.get_by_email(payload.email)
        if subscriber is None:
            subscriber = digest.subscriber_repo.create(payload.email)

    digest.subscription_repo.add(
        subscription=Subscription(
            subscriber_id=subscriber.id,
            entity_id=payload.entity_id,
            entity_type=payload.entity_type,
            target_type=payload.target_type,
        )
    )

    return {
        "status": "success",
        "message": f"{subscriber.email} subscribed to the digest.",
    }


@router.post("/digest/subscription/delete")
def delete_subscription(
    payload: SubscriptionDeleteRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    deleted = digest.subscription_repo.delete(payload.subscription_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Subscription with ID {payload.subscription_id} not found.",
        )

    return {
        "status": "success",
        "message": (
            f"Subscription {payload.subscription_id} unsubscribed "
            "from the digest."
        ),
    }