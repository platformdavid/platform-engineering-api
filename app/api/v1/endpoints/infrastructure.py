"""
Infrastructure endpoints for managing Terraform operations.

This module provides endpoints for infrastructure provisioning and management
using background tasks to avoid blocking API calls.
"""

import uuid
from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.infrastructure_service import InfrastructureService

router = APIRouter()


@router.post("/provision")
async def provision_infrastructure(
    service_name: str,
    service_type: str,
    environment: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Start infrastructure provisioning as a background task.
    
    This endpoint initiates infrastructure provisioning without blocking
    the API response. Use the operation status endpoint to check progress.
    
    Args:
        service_name: Name of the service
        service_type: Type of service (api, web, worker)
        environment: Environment (dev, staging, prod)
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Dict containing operation ID and status
    """
    # Generate unique operation ID
    operation_id = str(uuid.uuid4())
    
    # Initialize infrastructure service
    infrastructure_service = InfrastructureService()
    
    # Add background task
    background_tasks.add_task(
        infrastructure_service.provision_infrastructure_async,
        service_name=service_name,
        service_type=service_type,
        environment=environment,
        operation_id=operation_id
    )
    
    return {
        "operation_id": operation_id,
        "status": "started",
        "message": "Infrastructure provisioning started in background",
        "check_status_url": f"/api/v1/infrastructure/operations/{operation_id}"
    }


@router.post("/destroy")
async def destroy_infrastructure(
    service_name: str,
    environment: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Start infrastructure destruction as a background task.
    
    Args:
        service_name: Name of the service
        environment: Environment (dev, staging, prod)
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Dict containing operation ID and status
    """
    # Generate unique operation ID
    operation_id = str(uuid.uuid4())
    
    # Initialize infrastructure service
    infrastructure_service = InfrastructureService()
    
    # Add background task
    background_tasks.add_task(
        infrastructure_service.destroy_infrastructure_async,
        service_name=service_name,
        environment=environment,
        operation_id=operation_id
    )
    
    return {
        "operation_id": operation_id,
        "status": "started",
        "message": "Infrastructure destruction started in background",
        "check_status_url": f"/api/v1/infrastructure/operations/{operation_id}"
    }


@router.get("/operations/{operation_id}")
async def get_operation_status(
    operation_id: str,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the status of an infrastructure operation.
    
    Args:
        operation_id: Unique operation identifier
        db: Database session
        
    Returns:
        Dict containing operation status and details
    """
    infrastructure_service = InfrastructureService()
    operation_status = infrastructure_service.get_operation_status(operation_id)
    
    if not operation_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Operation {operation_id} not found"
        )
    
    return operation_status


@router.get("/operations")
async def list_operations(
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    List all active infrastructure operations.
    
    Args:
        db: Database session
        
    Returns:
        Dict containing all operation statuses
    """
    infrastructure_service = InfrastructureService()
    operations = infrastructure_service.list_operations()
    
    return {
        "operations": operations,
        "count": len(operations)
    }


@router.delete("/operations/cleanup")
async def cleanup_operations(
    max_age_hours: int = 24,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Clean up completed operations older than specified age.
    
    Args:
        max_age_hours: Maximum age in hours to keep operations
        db: Database session
        
    Returns:
        Dict containing cleanup results
    """
    infrastructure_service = InfrastructureService()
    cleaned_count = infrastructure_service.cleanup_completed_operations(max_age_hours)
    
    return {
        "message": f"Cleaned up {cleaned_count} completed operations",
        "cleaned_count": cleaned_count,
        "max_age_hours": max_age_hours
    }
