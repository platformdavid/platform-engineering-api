"""
Service repository for data access operations.

This module implements the repository pattern for Service entities.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service, ServiceType, Environment, ServiceStatus
from app.repositories.base import BaseRepository


class ServiceRepository(BaseRepository[Service]):
    """Repository for Service entities."""
    
    def __init__(self, db: AsyncSession):
        """Initialize ServiceRepository with database session."""
        super().__init__(db, Service)
    
    async def get_by_name(self, name: str) -> Optional[Service]:
        """Get service by name."""
        result = await self.db.execute(
            select(Service).where(Service.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_by_team(self, team: str, skip: int = 0, limit: int = 100) -> List[Service]:
        """Get services by team with pagination."""
        result = await self.db.execute(
            select(Service)
            .where(Service.team == team)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_type(self, service_type: ServiceType) -> List[Service]:
        """Get services by type."""
        result = await self.db.execute(
            select(Service).where(Service.service_type == service_type)
        )
        return result.scalars().all()
    
    async def get_by_environment(self, environment: Environment) -> List[Service]:
        """Get services by environment."""
        result = await self.db.execute(
            select(Service).where(Service.environment == environment)
        )
        return result.scalars().all()
    
    async def get_by_status(self, status: ServiceStatus) -> List[Service]:
        """Get services by status."""
        result = await self.db.execute(
            select(Service).where(Service.status == status)
        )
        return result.scalars().all()
    
    async def update_status(self, service_id: int, status: ServiceStatus) -> Optional[Service]:
        """Update service status."""
        service = await self.get_by_id(service_id)
        if service:
            service.status = status
            return await self.update(service)
        return None
    
    async def update_cicd_status(self, service_id: int, cicd_status: str) -> Optional[Service]:
        """Update CI/CD status."""
        service = await self.get_by_id(service_id)
        if service:
            service.cicd_status = cicd_status
            return await self.update(service)
        return None
    
    async def update_infrastructure_status(self, service_id: int, infrastructure_status: str) -> Optional[Service]:
        """Update infrastructure status."""
        service = await self.get_by_id(service_id)
        if service:
            service.infrastructure_status = infrastructure_status
            return await self.update(service)
        return None
    
    async def update_monitoring_status(self, service_id: int, monitoring_status: str) -> Optional[Service]:
        """Update monitoring status."""
        service = await self.get_by_id(service_id)
        if service:
            service.monitoring_status = monitoring_status
            return await self.update(service)
        return None
