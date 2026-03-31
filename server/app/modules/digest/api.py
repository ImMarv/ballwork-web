"""Thin API layer for digest module."""

from typing import Annotated

from app.db import get_db
from fastapi import APIRouter, Depends

from .deps.get_digest_service import get_digest_service
from .repository.models.subscription import Subscription
from .service import DigestService

router = APIRouter()


@router.post("/digest/subscriber")
def create_subscriber(
    email: str,
    digest: DigestService = Depends(get_digest_service),
):
    """Endpoint to create a subscriber for the digest.

    Args:
        email (str): The email address to subscribe to the digest.
        digest (DigestService, optional): The digest service. Defaults to Depends(get_digest_service).
    Returns:
        dict: A dictionary with the subscription status.
    """
    try:
        digest.subscriber_repo.create(email)
        return {"status": "success", "message": f"{email} subscribed to the digest."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/digest/unsubscribe")
def delete_subscriber(
    id: int,
    digest: DigestService = Depends(get_digest_service),
):
    """Endpoint to delete a subscriber for the digest.

    Args:
        id (int): The ID of the subscriber to delete.
        digest (DigestService, optional): The digest service. Defaults to Depends(get_digest_service).
    Returns:
        dict: A dictionary with the unsubscription status.
    """
    try:
        digest.subscriber_repo.delete(id)
        email = digest.subscriber_repo.get_by_id(id)
        return {
            "status": "success",
            "message": f"Email {email} with ID {id} unsubscribed and deleted from the digest.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/digest/subscription/add")
def create_subscription(
    subscriber_id: int,
    entity_id: int,
    entity_type: str,
    target_type: str,
    email: str,
    digest: DigestService = Depends(get_digest_service),
):
    """Endpoint to create a subscription for the digest.

    Args:
        email (str): The email address to subscribe to the digest.
        digest (DigestService, optional): The digest service. Defaults to Depends(get_digest_service).
    Returns:
        dict: A dictionary with the subscription status.
    """
    try:
        digest.subscription_repo.add(
            subscription=Subscription(
                subscriber_id=subscriber_id,
                entity_id=entity_id,
                entity_type=entity_type,
                target_type=target_type,
            )
        )
        return {"status": "success", "message": f"{email} subscribed to the digest."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/digest/subscription/delete")
def delete_subscription(
    subscription_id: int,
    digest: DigestService = Depends(get_digest_service),
):
    """Endpoint to delete a subscription for the digest.

    Args:
        subscription_id (int): The ID of the subscription to delete.
        digest (DigestService, optional): The digest service. Defaults to Depends(get_digest_service).
    Returns:
        dict: A dictionary with the unsubscription status.
    """
    try:
        digest.subscription_repo.delete(subscription_id)
        email = digest.subscriber_repo.get_by_id(subscription_id)
        return {
            "status": "success",
            "message": f"Email {email} with ID {subscription_id} unsubscribed from the digest.",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
