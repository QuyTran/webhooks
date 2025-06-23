"""
Main API router that includes all route modules.
"""
from fastapi import APIRouter

from app.api import webhooks

# Main API router
router = APIRouter()

# Include all route modules
router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
