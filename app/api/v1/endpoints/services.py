"""
Service endpoints for platform engineering API.

This module handles complete service lifecycle management.
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.service import (
    Service as ServiceSchema, 
    ServiceCreate, 
    ServiceUpdate, 
    ServiceProvision,
    ServiceTemplate
)
from app.services.platform_service import PlatformService

router = APIRouter()


@router.post("/", response_model=ServiceSchema)
async def create_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new service.
    
    This creates a service record but doesn't provision any resources yet.
    Use the /provision endpoint to set up CI/CD, infrastructure, and monitoring.
    
    Args:
        service_in: Service creation data
        db: Database session
        
    Returns:
        ServiceSchema: Created service data
        
    Raises:
        HTTPException: If service already exists
    """
    platform_service = PlatformService(db)
    existing_service = await platform_service.get_service_by_name(service_in.name)
    
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service with this name already exists"
        )
    
    service = await platform_service.create_service(service_in)
    return service


@router.post("/{service_id}/provision", response_model=ServiceSchema)
async def provision_service(
    service_id: int,
    provision_config: ServiceProvision,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Provision a complete service (CI/CD, infrastructure, monitoring).
    
    This endpoint orchestrates the provisioning of all service components:
    - CI/CD pipeline (GitHub Actions)
    - Infrastructure (AWS/Kubernetes)
    - Monitoring (Grafana/Prometheus)
    
    Args:
        service_id: Service ID
        provision_config: Provisioning configuration
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        ServiceSchema: Updated service with provisioning status
        
    Raises:
        HTTPException: If service not found or provisioning fails
    """
    platform_service = PlatformService(db)
    
    try:
        service = await platform_service.provision_service(service_id, provision_config)
        return service
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Provisioning failed: {str(e)}"
        )


@router.get("/", response_model=List[ServiceSchema])
async def read_services(
    skip: int = 0,
    limit: int = 100,
    team: str = None,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get list of services.
    
    Args:
        skip: Number of services to skip
        limit: Maximum number of services to return
        team: Filter by team (optional)
        db: Database session
        
    Returns:
        List[ServiceSchema]: List of services
    """
    platform_service = PlatformService(db)
    
    if team:
        services = await platform_service.get_services_by_team(team=team, skip=skip, limit=limit)
    else:
        services = await platform_service.get_all_services(skip=skip, limit=limit)
    
    return services


@router.get("/{service_id}", response_model=ServiceSchema)
async def read_service(
    service_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get service by ID.
    
    Args:
        service_id: Service ID
        db: Database session
        
    Returns:
        ServiceSchema: Service data
        
    Raises:
        HTTPException: If service not found
    """
    platform_service = PlatformService(db)
    service = await platform_service.get_service_by_id(service_id=service_id)
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return service


@router.put("/{service_id}", response_model=ServiceSchema)
async def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update service information.
    
    Args:
        service_id: Service ID
        service_in: Service update data
        db: Database session
        
    Returns:
        ServiceSchema: Updated service data
        
    Raises:
        HTTPException: If service not found
    """
    platform_service = PlatformService(db)
    service = await platform_service.update_service(service_id=service_id, service_in=service_in)
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return service


@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete a service and clean up all its resources.
    
    This will remove:
    - CI/CD pipeline
    - Infrastructure resources
    - Monitoring configuration
    - Logs and metrics
    
    Args:
        service_id: Service ID
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If service not found
    """
    platform_service = PlatformService(db)
    success = await platform_service.delete_service(service_id=service_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {"message": "Service deleted successfully"}


@router.get("/templates/list", response_model=List[ServiceTemplate])
async def list_service_templates() -> Any:
    """
    Get available service templates.
    
    Templates provide pre-configured settings for common service types.
    
    Returns:
        List[ServiceTemplate]: Available service templates
    """
    templates = [
        ServiceTemplate(
            name="fastapi-api",
            description="FastAPI REST API service",
            service_type="api",
            default_configuration={
                "framework": "fastapi",
                "port": 8000,
                "health_check": "/health"
            },
            default_infrastructure_config={
                "cpu": "500m",
                "memory": "512Mi",
                "replicas": 3,
                "autoscaling": True
            },
            default_monitoring_config={
                "metrics": ["http_requests", "response_time"],
                "alerts": ["high_error_rate", "high_latency"]
            },
            tags=["api", "fastapi", "rest"]
        ),
        ServiceTemplate(
            name="react-web",
            description="React web application",
            service_type="web",
            default_configuration={
                "framework": "react",
                "build_command": "npm run build",
                "serve_command": "npm start"
            },
            default_infrastructure_config={
                "cpu": "250m",
                "memory": "256Mi",
                "replicas": 2,
                "static_serving": True
            },
            default_monitoring_config={
                "metrics": ["page_load_time", "user_interactions"],
                "alerts": ["high_load_time"]
            },
            tags=["web", "react", "frontend"]
        ),
        ServiceTemplate(
            name="celery-worker",
            description="Celery background worker",
            service_type="worker",
            default_configuration={
                "framework": "celery",
                "broker": "redis",
                "concurrency": 4
            },
            default_infrastructure_config={
                "cpu": "1000m",
                "memory": "1Gi",
                "replicas": 2,
                "autoscaling": True
            },
            default_monitoring_config={
                "metrics": ["task_queue_length", "task_processing_time"],
                "alerts": ["queue_backlog", "worker_failures"]
            },
            tags=["worker", "celery", "background"]
        )
    ]
    
    return templates


@router.post("/from-template/{template_name}", response_model=ServiceSchema)
async def create_service_from_template(
    template_name: str,
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a service from a template.
    
    This combines template defaults with custom configuration.
    
    Args:
        template_name: Name of the template to use
        service_in: Service creation data (will be merged with template)
        db: Database session
        
    Returns:
        ServiceSchema: Created service data
        
    Raises:
        HTTPException: If template not found
    """
    # Get template
    templates = await list_service_templates()
    template = next((t for t in templates if t.name == template_name), None)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template '{template_name}' not found"
        )
    
    # Merge template with custom configuration
    merged_config = {**template.default_configuration, **service_in.configuration}
    merged_infra = {**template.default_infrastructure_config, **service_in.infrastructure_config}
    merged_monitoring = {**template.default_monitoring_config, **service_in.monitoring_config}
    
    # Create service with merged configuration
    service_data = ServiceCreate(
        name=service_in.name,
        team=service_in.team,
        service_type=template.service_type,
        environment=service_in.environment,
        description=service_in.description,
        tags=service_in.tags + template.tags,
        configuration=merged_config,
        infrastructure_config=merged_infra,
        monitoring_config=merged_monitoring
    )
    
    platform_service = PlatformService(db)
    service = await platform_service.create_service(service_data)
    
    return service
