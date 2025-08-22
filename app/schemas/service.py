"""
Service schemas for platform engineering API.

This module defines Pydantic schemas for service-related operations.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field

from app.models.service import ServiceType, Environment, ServiceStatus


class ServiceBase(BaseModel):
    """Base service schema with common fields."""
    
    name: str = Field(..., description="Service name (must be unique)")
    team: str = Field(..., description="Team that owns this service")
    service_type: ServiceType = Field(..., description="Type of service")
    environment: Environment = Field(..., description="Target environment")
    description: Optional[str] = Field(None, description="Service description")
    tags: List[str] = Field(default_factory=list, description="Service tags")


class ServiceCreate(ServiceBase):
    """Schema for creating a new service."""
    
    configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Service-specific configuration"
    )
    infrastructure_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Infrastructure configuration (AWS/K8s)"
    )
    monitoring_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Monitoring configuration (Grafana/Prometheus)"
    )


class ServiceUpdate(BaseModel):
    """Schema for updating service information."""
    
    name: Optional[str] = None
    team: Optional[str] = None
    service_type: Optional[ServiceType] = None
    environment: Optional[Environment] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    configuration: Optional[Dict[str, Any]] = None
    infrastructure_config: Optional[Dict[str, Any]] = None
    monitoring_config: Optional[Dict[str, Any]] = None


class Service(ServiceBase):
    """Schema for service response."""
    
    id: int
    status: ServiceStatus
    cicd_status: str
    infrastructure_status: str
    monitoring_status: str
    repository_url: Optional[str] = None
    deployment_url: Optional[str] = None
    monitoring_url: Optional[str] = None
    logs_url: Optional[str] = None
    configuration: Dict[str, Any]
    infrastructure_config: Dict[str, Any]
    monitoring_config: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ServiceProvision(BaseModel):
    """Schema for service provisioning request."""
    
    provision_cicd: bool = Field(True, description="Provision CI/CD pipeline")
    provision_infrastructure: bool = Field(True, description="Provision infrastructure")
    provision_monitoring: bool = Field(True, description="Provision monitoring")


class ServiceStatusUpdate(BaseModel):
    """Schema for service status updates."""
    
    status: ServiceStatus
    cicd_status: Optional[str] = None
    infrastructure_status: Optional[str] = None
    monitoring_status: Optional[str] = None
    deployment_url: Optional[str] = None
    monitoring_url: Optional[str] = None
    logs_url: Optional[str] = None
    message: Optional[str] = None


class ServiceTemplate(BaseModel):
    """Schema for service templates."""
    
    name: str
    description: str
    service_type: ServiceType
    default_configuration: Dict[str, Any]
    default_infrastructure_config: Dict[str, Any]
    default_monitoring_config: Dict[str, Any]
    tags: List[str] = Field(default_factory=list)
