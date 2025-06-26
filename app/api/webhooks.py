"""
Webhook routes for receiving SAP data.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import os
from logging.handlers import RotatingFileHandler

from app.auth import verify_api_key

# Configure logging
# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure file handler
file_handler = RotatingFileHandler(
    'logs/webhooks.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

router = APIRouter()

# Define custom headers to be returned with each response
CUSTOM_HEADERS = [
    {"name": "po", "value": "4500002481"}
]


class WebhookPayload(BaseModel):
    """Model for webhook payload data."""
    event_type: str
    entity_id: str
    data: Dict[str, Any]


class WebhookUpdate(BaseModel):
    """Model for webhook update data."""
    event_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


def add_custom_headers(response: Response):
    """Add custom headers to the response."""
    for header in CUSTOM_HEADERS:
        response.headers[header["name"]] = header["value"]
    return response


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def receive_webhook(
    payload: WebhookPayload,
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
):
    """
    Receive webhook data from SAP.

    This endpoint accepts webhook payloads from SAP systems,
    processes them, and returns an acknowledgement.
    """
    # Log request parameters
    query_params = dict(request.query_params)
    logger.info(f"POST Request Parameters: {query_params}")
    logger.info(f"POST Request Body: {payload.dict()}")

    # Add custom headers to response
    add_custom_headers(response)

    # Process the webhook data here
    # Example: Save to database, trigger a process, etc.

    return {"status": "accepted", "message": f"Webhook {payload.event_type} received"}


@router.get("/", status_code=status.HTTP_200_OK)
async def list_webhooks(
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
) -> List[Dict[str, Any]]:
    """
    List recent webhooks received.

    Returns a list of recently received webhooks for monitoring purposes.
    """
    # Log request parameters
    query_params = dict(request.query_params)
    logger.info(f"GET Request Parameters: {query_params}")

    # Add custom headers to response
    add_custom_headers(response)

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


@router.get("/{webhook_id}", status_code=status.HTTP_200_OK)
async def get_webhook(
    webhook_id: str,
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Get a specific webhook by ID.

    Returns details of a specific webhook.
    """
    # Log request parameters
    query_params = dict(request.query_params)
    logger.info(f"GET/{webhook_id} Request Parameters: {query_params}")

    # Add custom headers to response
    add_custom_headers(response)

    # In a real application, retrieve from database
    # This is just an example response
    webhook = {
        "id": webhook_id,
        "event_type": "order.created",
        "entity_id": "order123",
        "timestamp": "2023-09-15T10:30:00Z",
        "data": {
            "order_number": "ORD-12345",
            "customer_id": "CUST-789",
            "total_amount": 150.75
        }
    }

    return webhook


@router.put("/{webhook_id}", status_code=status.HTTP_200_OK)
async def update_webhook(
    webhook_id: str,
    payload: WebhookPayload,
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Update a webhook completely.

    Replaces all data for a specific webhook.
    """
    # Log request parameters and body
    query_params = dict(request.query_params)
    logger.info(f"PUT/{webhook_id} Request Parameters: {query_params}")
    logger.info(f"PUT/{webhook_id} Request Body: {payload.dict()}")

    # Add custom headers to response
    add_custom_headers(response)

    # In a real application, update in database
    # This is just an example response
    updated_webhook = {
        "id": webhook_id,
        "event_type": payload.event_type,
        "entity_id": payload.entity_id,
        "timestamp": "2023-09-15T11:45:00Z",
        "data": payload.data,
        "status": "updated"
    }

    return updated_webhook


@router.patch("/{webhook_id}", status_code=status.HTTP_200_OK)
async def partial_update_webhook(
    webhook_id: str,
    payload: WebhookUpdate,
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Update a webhook partially.

    Updates only the specified fields for a webhook.
    """
    # Log request parameters and body
    query_params = dict(request.query_params)
    logger.info(f"PATCH/{webhook_id} Request Parameters: {query_params}")
    logger.info(f"PATCH/{webhook_id} Request Body: {payload.dict()}")

    # Add custom headers to response
    add_custom_headers(response)

    # In a real application, update in database
    # This is just an example response
    updated_webhook = {
        "id": webhook_id,
        "event_type": payload.event_type if payload.event_type else "order.created",
        "entity_id": "order123",
        "timestamp": "2023-09-15T12:15:00Z",
        "data": payload.data if payload.data else {"status": "partially updated"},
        "status": "partially_updated"
    }

    return updated_webhook


@router.delete("/{webhook_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_webhook(
    webhook_id: str,
    request: Request,
    response: Response,
    _: bool = Depends(verify_api_key)
):
    """
    Delete a webhook.

    Removes a webhook from the system.
    """
    # Log request parameters
    query_params = dict(request.query_params)
    logger.info(f"DELETE/{webhook_id} Request Parameters: {query_params}")

    # Add custom headers to response
    add_custom_headers(response)

    # In a real application, delete from database
    # For DELETE, we return no content
    return None
