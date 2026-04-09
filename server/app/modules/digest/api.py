"""Thin API layer for digest module."""

from datetime import datetime
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


class DigestRunRequest(BaseModel):
    subscriber_id: int | None = None
    subscriber_email: EmailStr | None = None
    start: str  # ISO date string
    end: str  # ISO date string


class SubscriptionDeleteRequest(BaseModel):
    subscription_id: int


@router.post("/subscriber")
async def create_subscriber(
    payload: SubscriberCreateRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    digest.subscriber_repo.create(payload.email)
    return {
        "status": "success",
        "message": f"{payload.email} subscribed to the digest.",
    }


@router.post("/subscriber/delete")
async def delete_subscriber(
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
            f"Subscriber with ID {payload.subscriber_id} unsubscribed from the digest."
        ),
    }


@router.post("/subscription/add")
async def create_subscription(
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


@router.post("/subscription/delete")
async def delete_subscription(
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
            f"Subscription {payload.subscription_id} unsubscribed from the digest."
        ),
    }


@router.post("/run_job")
async def run_job(
    payload: DigestRunRequest,
    digest: Annotated[DigestService, Depends(get_digest_service)],
):
    # check if there is email but no ID
    if not payload.subscriber_id and payload.subscriber_email:
        subscriber = digest.subscriber_repo.get_by_email(payload.subscriber_email)
        if not subscriber:
            raise HTTPException(
                status_code=404,
                detail=f"Subscriber with email {payload.subscriber_email} not found.",
            )
        payload.subscriber_id = subscriber.id

    if payload.subscriber_id is None:
        raise HTTPException(
            status_code=400,
            detail="Either subscriber_id or subscriber_email must be provided.",
        )

    # parse string to datetime
    start_date = datetime.fromisoformat(payload.start)
    end_date = datetime.fromisoformat(payload.end)
    await digest.run_single_digest(
        subscriber_id=payload.subscriber_id, start=start_date, end=end_date
    )
    if not digest:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run digest job for {payload.start} to {payload.end}.",
        )
    return {
        "status": "success",
        "message": f"Digest job run for {payload.start} to {payload.end}.",
    }
