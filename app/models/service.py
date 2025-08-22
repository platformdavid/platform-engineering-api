"""
Service model for platform engineering tools.

This represents a complete service that includes CI/CD, infrastructure, and monitoring.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, JSON, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class ServiceType(str, enum.Enum):
    """Service types supported by the platform."""
    API = "api"
    WEB = "web"
    WORKER = "worker"
    DATABASE = "database"
    CACHE = "cache"


class Environment(str, enum.Enum):
    """Environment types."""
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class ServiceStatus(str, enum.Enum):
    """Service status."""
    PENDING = "pending"
    PROVISIONING = "provisioning"
    RUNNING = "running"
    FAILED = "failed"
    DEPRECATED = "deprecated"


class Service(Base):
    """
    Service model for platform engineering.
    
    Represents a complete service with all its components.
    """
    
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    team = Column(String, nullable=False)  # Which team owns this service
    service_type = Column(Enum(ServiceType), nullable=False)
    environment = Column(Enum(Environment), nullable=False)
    
    # Service configuration
    configuration = Column(JSON, nullable=False)  # Service-specific config
    infrastructure_config = Column(JSON, nullable=False)  # AWS/K8s config
    monitoring_config = Column(JSON, nullable=False)  # Grafana/Prometheus config
    
    # Status tracking
    status = Column(Enum(ServiceStatus), default=ServiceStatus.PENDING)
    cicd_status = Column(String, default="not_configured")  # CI/CD pipeline status
    infrastructure_status = Column(String, default="not_provisioned")  # AWS/K8s status
    monitoring_status = Column(String, default="not_configured")  # Monitoring status
    
    # URLs and endpoints
    repository_url = Column(String, nullable=True)  # Git repository
    deployment_url = Column(String, nullable=True)  # Service endpoint
    monitoring_url = Column(String, nullable=True)  # Grafana dashboard
    logs_url = Column(String, nullable=True)  # Log aggregation
    
    # Metadata
    description = Column(Text, nullable=True)
    tags = Column(JSON, default=list)  # Service tags for organization
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        """String representation of the Service model."""
        return f"<Service(id={self.id}, name='{self.name}', team='{self.team}')>"
