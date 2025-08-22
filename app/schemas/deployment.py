"""
Deployment schemas for platform engineering API.

This module defines Pydantic schemas for deployment-related operations.
"""

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel


class DeploymentBase(BaseModel):
    """Base deployment schema with common fields."""
    
    name: str
    team: str
    environment: str
    service_type: str
    configuration: Dict[str, Any]


class DeploymentCreate(DeploymentBase):
    """Schema for creating a new deployment."""
    pass


class DeploymentUpdate(BaseModel):
    """Schema for updating deployment information."""
    
    name: Optional[str] = None
    team: Optional[str] = None
    environment: Optional[str] = None
    service_type: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class Deployment(DeploymentBase):
    """Schema for deployment response."""
    
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DeploymentStatus(BaseModel):
    """Schema for deployment status updates."""
    
    status: str
    message: Optional[str] = None
