"""
Base repository for data access operations.

This module provides a simple base repository pattern following Python conventions.
"""

from typing import List, Optional, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.base import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """
    Base repository following Python conventions.
    
    Provides common CRUD operations for all entities.
    """
    
    def __init__(self, db: AsyncSession, model: type):
        """
        Initialize repository with database session and model.
        
        Args:
            db: Database session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model
    
    async def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination."""
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        await self.db.commit()
        await self.db.refresh(entity)
        return entity
    
    async def delete(self, entity: T) -> bool:
        """Delete an entity."""
        await self.db.delete(entity)
        await self.db.commit()
        return True
    
    async def delete_by_id(self, id: int) -> bool:
        """Delete entity by ID."""
        entity = await self.get_by_id(id)
        if entity:
            return await self.delete(entity)
        return False
