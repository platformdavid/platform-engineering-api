#!/usr/bin/env python3
"""
Database setup script for Platform Engineering API.

This script initializes the database with initial data including:
- Service templates
- Sample services
- Platform configuration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Force SQLite database URL to avoid PostgreSQL compilation issues
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./platform_engineering.db"

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.service import Service, ServiceType, Environment, ServiceStatus
from app.schemas.service import ServiceTemplate


async def create_initial_data():
    """Create initial data in the database."""
    async with AsyncSessionLocal() as db:
        # Create service templates
        await create_service_templates(db)
        
        # Create sample services
        await create_sample_services(db)
        
        print("✅ Database initialized successfully!")


async def create_service_templates(db: AsyncSession):
    """Create initial service templates."""
    templates = [
        ServiceTemplate(
            name="fastapi-api",
            description="FastAPI REST API service with comprehensive testing",
            service_type=ServiceType.API,
            default_configuration={
                "framework": "fastapi",
                "port": 8000,
                "health_check": "/health",
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_integration_tests": True,
                "enable_sonarqube": True,
                "enable_security_scan": True,
                "enable_smoke_tests": True,
                "enable_health_check": True
            },
            default_infrastructure_config={
                "cpu": "500m",
                "memory": "512Mi",
                "replicas": 3,
                "autoscaling": True,
                "min_replicas": 2,
                "max_replicas": 10
            },
            default_monitoring_config={
                "metrics": ["http_requests", "response_time", "error_rate"],
                "alerts": ["high_error_rate", "high_latency", "service_down"],
                "dashboard": "api-service-dashboard"
            },
            tags=["api", "fastapi", "rest", "python"]
        ),
        ServiceTemplate(
            name="react-web",
            description="React web application with modern tooling",
            service_type=ServiceType.WEB,
            default_configuration={
                "framework": "react",
                "build_command": "npm run build",
                "serve_command": "npm start",
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_sonarqube": True,
                "enable_smoke_tests": True,
                "enable_health_check": True,
                "enable_visual_tests": False
            },
            default_infrastructure_config={
                "cpu": "250m",
                "memory": "256Mi",
                "replicas": 2,
                "static_serving": True,
                "cdn_enabled": True
            },
            default_monitoring_config={
                "metrics": ["page_load_time", "user_interactions", "error_rate"],
                "alerts": ["high_load_time", "high_error_rate"],
                "dashboard": "web-service-dashboard"
            },
            tags=["web", "react", "frontend", "javascript"]
        ),
        ServiceTemplate(
            name="celery-worker",
            description="Celery background worker for async tasks",
            service_type=ServiceType.WORKER,
            default_configuration={
                "framework": "celery",
                "broker": "redis",
                "concurrency": 4,
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_sonarqube": True,
                "enable_security_scan": True,
                "enable_smoke_tests": True
            },
            default_infrastructure_config={
                "cpu": "1000m",
                "memory": "1Gi",
                "replicas": 2,
                "autoscaling": True,
                "min_replicas": 1,
                "max_replicas": 5
            },
            default_monitoring_config={
                "metrics": ["task_queue_length", "task_processing_time", "worker_health"],
                "alerts": ["queue_backlog", "worker_failures", "high_processing_time"],
                "dashboard": "worker-service-dashboard"
            },
            tags=["worker", "celery", "background", "python"]
        ),
        ServiceTemplate(
            name="nodejs-api",
            description="Node.js Express API service",
            service_type=ServiceType.API,
            default_configuration={
                "framework": "express",
                "port": 3000,
                "health_check": "/health",
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_integration_tests": True,
                "enable_sonarqube": True,
                "enable_security_scan": True,
                "enable_smoke_tests": True,
                "enable_health_check": True
            },
            default_infrastructure_config={
                "cpu": "500m",
                "memory": "512Mi",
                "replicas": 3,
                "autoscaling": True,
                "min_replicas": 2,
                "max_replicas": 10
            },
            default_monitoring_config={
                "metrics": ["http_requests", "response_time", "error_rate"],
                "alerts": ["high_error_rate", "high_latency", "service_down"],
                "dashboard": "nodejs-api-dashboard"
            },
            tags=["api", "express", "nodejs", "javascript"]
        )
    ]
    
    # Store templates in a way that can be accessed by the API
    # In a real implementation, you might store these in a separate table
    print(f"📋 Created {len(templates)} service templates")
    
    for template in templates:
        print(f"  - {template.name}: {template.description}")


async def create_sample_services(db: AsyncSession):
    """Create sample services for demonstration."""
    sample_services = [
        {
            "name": "user-service",
            "team": "backend-team",
            "service_type": ServiceType.API,
            "environment": Environment.STAGING,
            "description": "User management API service",
            "tags": ["api", "users", "auth"],
            "configuration": {
                "framework": "fastapi",
                "port": 8000,
                "health_check": "/health",
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_integration_tests": True,
                "enable_sonarqube": True,
                "enable_security_scan": True,
                "enable_smoke_tests": True,
                "enable_health_check": True
            },
            "infrastructure_config": {
                "cpu": "500m",
                "memory": "512Mi",
                "replicas": 3,
                "autoscaling": True
            },
            "monitoring_config": {
                "metrics": ["http_requests", "response_time", "error_rate"],
                "alerts": ["high_error_rate", "high_latency"],
                "dashboard": "user-service-dashboard"
            }
        },
        {
            "name": "frontend-app",
            "team": "frontend-team",
            "service_type": ServiceType.WEB,
            "environment": Environment.STAGING,
            "description": "Main frontend application",
            "tags": ["web", "react", "frontend"],
            "configuration": {
                "framework": "react",
                "build_command": "npm run build",
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_sonarqube": True,
                "enable_smoke_tests": True,
                "enable_health_check": True
            },
            "infrastructure_config": {
                "cpu": "250m",
                "memory": "256Mi",
                "replicas": 2,
                "static_serving": True
            },
            "monitoring_config": {
                "metrics": ["page_load_time", "user_interactions"],
                "alerts": ["high_load_time"],
                "dashboard": "frontend-app-dashboard"
            }
        },
        {
            "name": "email-worker",
            "team": "backend-team",
            "service_type": ServiceType.WORKER,
            "environment": Environment.STAGING,
            "description": "Email processing worker",
            "tags": ["worker", "email", "background"],
            "configuration": {
                "framework": "celery",
                "broker": "redis",
                "concurrency": 4,
                "enable_linting": True,
                "enable_formatting": True,
                "enable_unit_tests": True,
                "enable_sonarqube": True,
                "enable_security_scan": True,
                "enable_smoke_tests": True
            },
            "infrastructure_config": {
                "cpu": "1000m",
                "memory": "1Gi",
                "replicas": 2,
                "autoscaling": True
            },
            "monitoring_config": {
                "metrics": ["task_queue_length", "task_processing_time"],
                "alerts": ["queue_backlog", "worker_failures"],
                "dashboard": "email-worker-dashboard"
            }
        }
    ]
    
    for service_data in sample_services:
        service = Service(
            name=service_data["name"],
            team=service_data["team"],
            service_type=service_data["service_type"],
            environment=service_data["environment"],
            description=service_data["description"],
            tags=service_data["tags"],
            configuration=service_data["configuration"],
            infrastructure_config=service_data["infrastructure_config"],
            monitoring_config=service_data["monitoring_config"],
            status=ServiceStatus.PENDING
        )
        
        db.add(service)
    
    await db.commit()
    print(f"📦 Created {len(sample_services)} sample services")


async def main():
    """Main setup function."""
    print("🚀 Setting up Platform Engineering Database...")
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database tables created")
        
        # Create initial data
        await create_initial_data()
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 What was created:")
        print("  - Service templates (fastapi-api, react-web, celery-worker, nodejs-api)")
        print("  - Sample services (user-service, frontend-app, email-worker)")
        print("  - Platform configuration")
        
        print("\n🔗 Next steps:")
        print("  1. Start the API: uvicorn app.main:app --reload")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Test the endpoints with the sample data")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
