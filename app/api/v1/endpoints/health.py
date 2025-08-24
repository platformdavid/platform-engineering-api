"""
Health check endpoints for the PlatformDavid Platform Engineering API.

This module provides health check endpoints for monitoring and deployment.
"""

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

router = APIRouter()


@router.get("/")
async def health_check() -> Any:
    """
    Basic health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "service": "PlatformDavid Platform Engineering API",
        "version": "1.0.0"
    }


@router.get("/live")
async def liveness_check() -> Any:
    """
    Liveness check for Kubernetes.
    
    Returns:
        dict: Liveness status
    """
    return {"status": "alive"}


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)) -> Any:
    """
    Readiness check for Kubernetes.
    
    Checks database connectivity and other dependencies.
    
    Args:
        db: Database session
        
    Returns:
        dict: Readiness status
    """
    try:
        # Test database connection
        await db.execute("SELECT 1")
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e)
        }
