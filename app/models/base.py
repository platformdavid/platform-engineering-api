"""
Base model for all entities.

This module provides a base model class with common fields.
"""

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel(Base):
    """Base model class for all entities."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        """String representation of the entity."""
        return f"<{self.__class__.__name__}(id={self.id})>"
