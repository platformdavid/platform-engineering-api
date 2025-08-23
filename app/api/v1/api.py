"""
Main API router for v1 endpoints.

This module includes all API routes for version 1 of the API.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import deployments, services, health, infrastructure

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(deployments.router, prefix="/deployments", tags=["deployments"])
api_router.include_router(services.router, prefix="/services", tags=["services"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(infrastructure.router, prefix="/infrastructure", tags=["infrastructure"])
