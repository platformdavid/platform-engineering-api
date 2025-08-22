"""
Service mapper for entity-to-DTO conversion.

This module provides mapping functionality for converting between
Service entities and DTOs.
"""

from typing import List
from datetime import datetime

from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate, Service as ServiceDto


class ServiceMapper:
    """Mapper for Service entities and DTOs."""
    
    @staticmethod
    def entity_to_dto(entity: Service) -> ServiceDto:
        """Convert Service entity to Service DTO."""
        return ServiceDto(
            id=entity.id,
            name=entity.name,
            team=entity.team,
            service_type=entity.service_type,
            environment=entity.environment,
            description=entity.description,
            tags=entity.tags,
            status=entity.status,
            cicd_status=entity.cicd_status,
            infrastructure_status=entity.infrastructure_status,
            monitoring_status=entity.monitoring_status,
            repository_url=entity.repository_url,
            deployment_url=entity.deployment_url,
            monitoring_url=entity.monitoring_url,
            logs_url=entity.logs_url,
            configuration=entity.configuration,
            infrastructure_config=entity.infrastructure_config,
            monitoring_config=entity.monitoring_config,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    @staticmethod
    def dto_to_entity(dto: ServiceCreate) -> Service:
        """Convert ServiceCreate DTO to Service entity."""
        return Service(
            name=dto.name,
            team=dto.team,
            service_type=dto.service_type,
            environment=dto.environment,
            description=dto.description,
            tags=dto.tags,
            configuration=dto.configuration,
            infrastructure_config=dto.infrastructure_config,
            monitoring_config=dto.monitoring_config,
            status="pending",
            cicd_status="pending",
            infrastructure_status="pending",
            monitoring_status="pending"
        )
    
    @staticmethod
    def update_entity_from_dto(entity: Service, dto: ServiceUpdate) -> Service:
        """Update Service entity from ServiceUpdate DTO."""
        update_data = dto.dict(exclude_unset=True)
        
        for field, value in update_data.items():
            if hasattr(entity, field):
                setattr(entity, field, value)
        
        entity.updated_at = datetime.utcnow()
        return entity
    
    @staticmethod
    def entities_to_dtos(entities: List[Service]) -> List[ServiceDto]:
        """Convert list of Service entities to list of Service DTOs."""
        return [ServiceMapper.entity_to_dto(entity) for entity in entities]
