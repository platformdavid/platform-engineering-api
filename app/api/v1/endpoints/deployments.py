"""
Deployment endpoints for platform engineering API.

This module handles deployment CRUD operations for internal tools.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.deployment import Deployment as DeploymentSchema, DeploymentCreate, DeploymentUpdate
from app.services.deployment_service import DeploymentService

router = APIRouter()


@router.post("/", response_model=DeploymentSchema)
async def create_deployment(
    deployment_in: DeploymentCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new deployment configuration.
    
    Args:
        deployment_in: Deployment creation data
        db: Database session
        
    Returns:
        DeploymentSchema: Created deployment data
        
    Raises:
        HTTPException: If deployment already exists
    """
    deployment_service = DeploymentService(db)
    existing_deployment = await deployment_service.get_deployment_by_name(name=deployment_in.name)
    
    if existing_deployment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deployment with this name already exists"
        )
    
    deployment = await deployment_service.create_deployment(deployment_in)
    return deployment


@router.get("/", response_model=List[DeploymentSchema])
async def read_deployments(
    skip: int = 0,
    limit: int = 100,
    team: str = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get list of deployments.
    
    Args:
        skip: Number of deployments to skip
        limit: Maximum number of deployments to return
        team: Filter by team (optional)
        db: Database session
        
    Returns:
        List[DeploymentSchema]: List of deployments
    """
    deployment_service = DeploymentService(db)
    
    if team:
        deployments = await deployment_service.get_deployments_by_team(team=team, skip=skip, limit=limit)
    else:
        deployments = await deployment_service.get_all_deployments(skip=skip, limit=limit)
    
    return deployments


@router.get("/{deployment_id}", response_model=DeploymentSchema)
async def read_deployment(
    deployment_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get deployment by ID.
    
    Args:
        deployment_id: Deployment ID
        db: Database session
        
    Returns:
        DeploymentSchema: Deployment data
        
    Raises:
        HTTPException: If deployment not found
    """
    deployment_service = DeploymentService(db)
    deployment = await deployment_service.get_deployment_by_id(deployment_id=deployment_id)
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    return deployment


@router.put("/{deployment_id}", response_model=DeploymentSchema)
async def update_deployment(
    deployment_id: int,
    deployment_in: DeploymentUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update deployment information.
    
    Args:
        deployment_id: Deployment ID
        deployment_in: Deployment update data
        db: Database session
        
    Returns:
        DeploymentSchema: Updated deployment data
        
    Raises:
        HTTPException: If deployment not found
    """
    deployment_service = DeploymentService(db)
    deployment = await deployment_service.update_deployment(deployment_id=deployment_id, deployment_in=deployment_in)
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    return deployment


@router.delete("/{deployment_id}")
async def delete_deployment(
    deployment_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete a deployment.
    
    Args:
        deployment_id: Deployment ID
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If deployment not found
    """
    deployment_service = DeploymentService(db)
    success = await deployment_service.delete_deployment(deployment_id=deployment_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    return {"message": "Deployment deleted successfully"}


@router.post("/{deployment_id}/trigger")
async def trigger_deployment(
    deployment_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Trigger a deployment (simulate deployment process).
    
    Args:
        deployment_id: Deployment ID
        db: Database session
        
    Returns:
        dict: Deployment status
        
    Raises:
        HTTPException: If deployment not found
    """
    deployment_service = DeploymentService(db)
    deployment = await deployment_service.get_deployment_by_id(deployment_id=deployment_id)
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Simulate deployment process
    await deployment_service.update_deployment_status(
        deployment_id=deployment_id,
        status="running",
        message="Deployment started"
    )
    
    return {
        "message": "Deployment triggered successfully",
        "deployment_id": deployment_id,
        "status": "running"
    }
