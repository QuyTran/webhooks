"""
Webhook routes for receiving SAP data.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from typing import Dict, Any, List

from app.auth import verify_api_key

router = APIRouter()


class WebhookPayload(BaseModel):
    """Model for webhook payload data."""
    event_type: str
    entity_id: str
    data: Dict[str, Any]


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(
    payload: WebhookPayload,
    request: Request,
    _: bool = Depends(verify_api_key)
):
    """
    Receive webhook data from SAP.

    This endpoint accepts webhook payloads from SAP systems,
    processes them, and returns an acknowledgement.
    """
    # Process the webhook data here
    # Example: Save to database, trigger a process, etc.

    # Log the received webhook (example)
    print(f"Received webhook: {payload.event_type} for {payload.entity_id}")

    return {"status": "accepted", "message": f"Webhook {payload.event_type} received"}


@router.get("/", status_code=status.HTTP_200_OK)
async def list_webhooks(_: bool = Depends(verify_api_key)) -> List[Dict[str, Any]]:
    """
    List recent webhooks received.

    Returns a list of recently received webhooks for monitoring purposes.
    """
    # In a real application, retrieve from database or cache
    # This is just an example response
    recent_webhooks = [
        {
            "id": "webhook123",
            "event_type": "order.created",
            "entity_id": "order123",
            "timestamp": "2023-09-15T10:30:00Z"
        },
        {
            "id": "webhook124",
            "event_type": "inventory.updated",
            "entity_id": "product456",
            "timestamp": "2023-09-15T10:35:00Z"
        }
    ]

    return recent_webhooks
