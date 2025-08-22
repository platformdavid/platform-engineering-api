"""
Deployment service for platform engineering API.

This module contains business logic for deployment operations.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deployment import Deployment
from app.schemas.deployment import DeploymentCreate, DeploymentUpdate


class DeploymentService:
    """
    Service class for deployment-related business logic.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize DeploymentService with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_deployment_by_id(self, deployment_id: int) -> Optional[Deployment]:
        """
        Get deployment by ID.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Optional[Deployment]: Deployment if found, None otherwise
        """
        result = await self.db.execute(select(Deployment).where(Deployment.id == deployment_id))
        return result.scalar_one_or_none()
    
    async def get_deployment_by_name(self, name: str) -> Optional[Deployment]:
        """
        Get deployment by name.
        
        Args:
            name: Deployment name
            
        Returns:
            Optional[Deployment]: Deployment if found, None otherwise
        """
        result = await self.db.execute(select(Deployment).where(Deployment.name == name))
        return result.scalar_one_or_none()
    
    async def get_deployments_by_team(self, team: str, skip: int = 0, limit: int = 100) -> List[Deployment]:
        """
        Get deployments by team with pagination.
        
        Args:
            team: Team name
            skip: Number of deployments to skip
            limit: Maximum number of deployments to return
            
        Returns:
            List[Deployment]: List of deployments
        """
        result = await self.db.execute(
            select(Deployment)
            .where(Deployment.team == team)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all_deployments(self, skip: int = 0, limit: int = 100) -> List[Deployment]:
        """
        Get all deployments with pagination.
        
        Args:
            skip: Number of deployments to skip
            limit: Maximum number of deployments to return
            
        Returns:
            List[Deployment]: List of deployments
        """
        result = await self.db.execute(
            select(Deployment).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create_deployment(self, deployment_in: DeploymentCreate) -> Deployment:
        """
        Create a new deployment.
        
        Args:
            deployment_in: Deployment creation data
            
        Returns:
            Deployment: Created deployment
        """
        db_deployment = Deployment(
            name=deployment_in.name,
            team=deployment_in.team,
            environment=deployment_in.environment,
            service_type=deployment_in.service_type,
            configuration=deployment_in.configuration,
            status="pending"
        )
        
        self.db.add(db_deployment)
        await self.db.commit()
        await self.db.refresh(db_deployment)
        
        return db_deployment
    
    async def update_deployment(self, deployment_id: int, deployment_in: DeploymentUpdate) -> Optional[Deployment]:
        """
        Update deployment information.
        
        Args:
            deployment_id: Deployment ID
            deployment_in: Deployment update data
            
        Returns:
            Optional[Deployment]: Updated deployment if found, None otherwise
        """
        deployment = await self.get_deployment_by_id(deployment_id)
        if not deployment:
            return None
        
        update_data = deployment_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(deployment, field, value)
        
        await self.db.commit()
        await self.db.refresh(deployment)
        
        return deployment
    
    async def update_deployment_status(self, deployment_id: int, status: str, message: str = None) -> Optional[Deployment]:
        """
        Update deployment status.
        
        Args:
            deployment_id: Deployment ID
            status: New status
            message: Optional status message
            
        Returns:
            Optional[Deployment]: Updated deployment if found, None otherwise
        """
        deployment = await self.get_deployment_by_id(deployment_id)
        if not deployment:
            return None
        
        deployment.status = status
        if message:
            # You could add a message field to the model if needed
            pass
        
        await self.db.commit()
        await self.db.refresh(deployment)
        
        return deployment
    
    async def delete_deployment(self, deployment_id: int) -> bool:
        """
        Delete a deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            bool: True if deployment was deleted, False if not found
        """
        deployment = await self.get_deployment_by_id(deployment_id)
        if not deployment:
            return False
        
        await self.db.delete(deployment)
        await self.db.commit()
        
        return True
