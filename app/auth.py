"""
Authentication utilities for API security.
"""
from fastapi import Depends, HTTPException, Header, status
from typing import Optional

from app.config import settings


async def verify_api_key(api_key: Optional[str] = Header(None)) -> bool:
    """
    Verify if the provided API key is valid.

    Args:
        api_key: The API key provided in the request header.

    Returns:
        bool: True if the API key is valid.

    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if settings.API_KEY is None:
        # If no API key is configured, authentication is disabled
        return True

    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return True
