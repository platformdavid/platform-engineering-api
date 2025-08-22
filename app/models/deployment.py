"""
Deployment model for platform engineering tools.

This represents a deployment configuration that can be used by multiple teams.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, JSON
from sqlalchemy.sql import func

from app.core.database import Base


class Deployment(Base):
    """
    Deployment model for platform engineering.
    
    Represents deployment configurations that can be shared across teams.
    """
    
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    team = Column(String, nullable=False)  # Which team owns this deployment
    environment = Column(String, nullable=False)  # dev, staging, prod
    service_type = Column(String, nullable=False)  # web, api, worker, etc.
    configuration = Column(JSON, nullable=False)  # Deployment config
    status = Column(String, default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self) -> str:
        """String representation of the Deployment model."""
        return f"<Deployment(id={self.id}, name='{self.name}', team='{self.team}')>"
