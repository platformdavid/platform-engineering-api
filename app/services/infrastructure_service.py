"""
Infrastructure service for managing Terraform operations.

This service handles infrastructure provisioning as background tasks,
separating infrastructure concerns from API endpoints.
"""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import json

from app.services.terraform_service import TerraformService
from app.config import settings


class InfrastructureService:
    """
    Infrastructure service for managing Terraform operations.
    
    This service handles infrastructure provisioning as background tasks
    to avoid blocking API endpoints and improve security.
    """
    
    def __init__(self):
        """Initialize infrastructure service."""
        self.terraform_service = TerraformService()
        self._active_operations: Dict[str, Dict[str, Any]] = {}
    
    async def provision_infrastructure_async(
        self, 
        service_name: str, 
        service_type: str, 
        environment: str,
        operation_id: str
    ) -> None:
        """
        Provision infrastructure asynchronously.
        
        This method runs Terraform operations in the background
        and updates the operation status.
        
        Args:
            service_name: Name of the service
            service_type: Type of service (api, web, worker)
            environment: Environment (dev, staging, prod)
            operation_id: Unique operation identifier
        """
        # Initialize operation status
        self._active_operations[operation_id] = {
            "status": "running",
            "started_at": datetime.utcnow().isoformat(),
            "service_name": service_name,
            "service_type": service_type,
            "environment": environment,
            "progress": "Initializing Terraform...",
            "outputs": {},
            "error": None
        }
        
        try:
            # Update progress
            self._active_operations[operation_id]["progress"] = "Generating Terraform configuration..."
            
            # Create infrastructure
            result = await self.terraform_service.create_infrastructure(
                service_name=service_name,
                service_type=service_type,
                environment=environment
            )
            
            if result["status"] == "success":
                self._active_operations[operation_id].update({
                    "status": "completed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "progress": "Infrastructure provisioned successfully",
                    "outputs": result.get("outputs", {}),
                    "cost_breakdown": result.get("cost_breakdown", {})
                })
            else:
                self._active_operations[operation_id].update({
                    "status": "failed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "progress": "Infrastructure provisioning failed",
                    "error": result.get("message", "Unknown error")
                })
                
        except Exception as e:
            self._active_operations[operation_id].update({
                "status": "failed",
                "completed_at": datetime.utcnow().isoformat(),
                "progress": "Infrastructure provisioning failed",
                "error": str(e)
            })
    
    async def destroy_infrastructure_async(
        self, 
        service_name: str, 
        environment: str,
        operation_id: str
    ) -> None:
        """
        Destroy infrastructure asynchronously.
        
        Args:
            service_name: Name of the service
            environment: Environment (dev, staging, prod)
            operation_id: Unique operation identifier
        """
        # Initialize operation status
        self._active_operations[operation_id] = {
            "status": "running",
            "started_at": datetime.utcnow().isoformat(),
            "service_name": service_name,
            "environment": environment,
            "progress": "Initializing Terraform destroy...",
            "outputs": {},
            "error": None
        }
        
        try:
            # Update progress
            self._active_operations[operation_id]["progress"] = "Destroying infrastructure..."
            
            # Destroy infrastructure
            result = await self.terraform_service.destroy_infrastructure(
                service_name=service_name,
                environment=environment
            )
            
            if result["status"] == "success":
                self._active_operations[operation_id].update({
                    "status": "completed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "progress": "Infrastructure destroyed successfully",
                    "cost_savings": result.get("cost_savings", "100%")
                })
            else:
                self._active_operations[operation_id].update({
                    "status": "failed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "progress": "Infrastructure destruction failed",
                    "error": result.get("message", "Unknown error")
                })
                
        except Exception as e:
            self._active_operations[operation_id].update({
                "status": "failed",
                "completed_at": datetime.utcnow().isoformat(),
                "progress": "Infrastructure destruction failed",
                "error": str(e)
            })
    
    def get_operation_status(self, operation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of an infrastructure operation.
        
        Args:
            operation_id: Unique operation identifier
            
        Returns:
            Operation status or None if not found
        """
        return self._active_operations.get(operation_id)
    
    def list_operations(self) -> Dict[str, Dict[str, Any]]:
        """
        List all active infrastructure operations.
        
        Returns:
            Dictionary of operation statuses
        """
        return self._active_operations.copy()
    
    def cleanup_completed_operations(self, max_age_hours: int = 24) -> int:
        """
        Clean up completed operations older than specified age.
        
        Args:
            max_age_hours: Maximum age in hours to keep operations
            
        Returns:
            Number of operations cleaned up
        """
        current_time = datetime.utcnow()
        operations_to_remove = []
        
        for operation_id, operation in self._active_operations.items():
            if operation["status"] in ["completed", "failed"]:
                completed_at = datetime.fromisoformat(operation["completed_at"])
                age_hours = (current_time - completed_at).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    operations_to_remove.append(operation_id)
        
        for operation_id in operations_to_remove:
            del self._active_operations[operation_id]
        
        return len(operations_to_remove)
