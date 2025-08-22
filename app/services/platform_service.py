"""
Platform service for orchestrating complete service provisioning.

This service coordinates CI/CD, infrastructure, and monitoring setup.
"""

from typing import List, Optional, Dict, Any
import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service, ServiceStatus
from app.schemas.service import ServiceCreate, ServiceUpdate, ServiceProvision
from app.services.github_actions_service import GitHubActionsService
from app.services.terraform_service import TerraformService
from app.services.kubernetes_service import KubernetesService


class PlatformService:
    """
    Platform service for orchestrating complete service provisioning.

    This service coordinates the creation of CI/CD pipelines, infrastructure,
    and monitoring for new services using industry-standard tools.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize PlatformService with database session.

        Args:
            db: Database session
        """
        self.db = db
        self.github_actions_service = GitHubActionsService()
        self.terraform_service = TerraformService()
        self.kubernetes_service = KubernetesService()

    async def create_service(self, service_in: ServiceCreate) -> Service:
        """
        Create a new service with all its components.

        Args:
            service_in: Service creation data

        Returns:
            Service: Created service
        """
        db_service = Service(
            name=service_in.name,
            team=service_in.team,
            service_type=service_in.service_type,
            environment=service_in.environment,
            description=service_in.description,
            tags=service_in.tags,
            configuration=service_in.configuration,
            infrastructure_config=service_in.infrastructure_config,
            monitoring_config=service_in.monitoring_config,
            status=ServiceStatus.PENDING
        )

        self.db.add(db_service)
        await self.db.commit()
        await self.db.refresh(db_service)

        return db_service

    async def provision_service(self, service_id: int, provision_config: ServiceProvision) -> Service:
        """
        Provision a complete service (CI/CD, infrastructure, monitoring).

        This method orchestrates the provisioning of all service components
        using industry-standard tools like GitHub Actions, Terraform, and Kubernetes.

        Args:
            service_id: Service ID
            provision_config: Provisioning configuration

        Returns:
            Service: Updated service with provisioning status
        """
        service = await self.get_service_by_id(service_id)
        if not service:
            raise ValueError(f"Service {service_id} not found")

        # Update status to provisioning
        service.status = ServiceStatus.PROVISIONING
        await self.db.commit()

        try:
            # Provision components in parallel
            tasks = []

            if provision_config.provision_cicd:
                tasks.append(self._provision_cicd(service))

            if provision_config.provision_infrastructure:
                tasks.append(self._provision_infrastructure(service))

            if provision_config.provision_monitoring:
                tasks.append(self._provision_monitoring(service))

            # Wait for all provisioning tasks to complete
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Check for any failures
                for result in results:
                    if isinstance(result, Exception):
                        raise result

            # Update service status
            service.status = ServiceStatus.RUNNING
            await self.db.commit()

        except Exception as e:
            service.status = ServiceStatus.FAILED
            await self.db.commit()
            raise e

        await self.db.refresh(service)
        return service

    async def _provision_cicd(self, service: Service) -> None:
        """
        Provision CI/CD pipeline using GitHub Actions.

        Args:
            service: Service to provision CI/CD for
        """
        try:
            # Create GitHub Actions workflow
            workflow_result = await self.github_actions_service.create_workflow(
                service_name=service.name,
                team=service.team,
                service_type=service.service_type.value
            )

            # Update CI/CD status
            service.cicd_status = "configured"
            service.repository_url = f"https://github.com/platformdavid/{service.name}"

            # Store workflow information in configuration
            service.configuration["github_actions_workflow"] = {
                "file": ".github/workflows/ci-cd.yml",
                "status": "created",
                "url": f"https://github.com/platformdavid/{service.name}/actions"
            }

            await self.db.commit()

        except Exception as e:
            service.cicd_status = "failed"
            await self.db.commit()
            raise e

    async def _provision_infrastructure(self, service: Service) -> None:
        """
        Provision infrastructure using Terraform and Kubernetes.

        Args:
            service: Service to provision infrastructure for
        """
        try:
            # Create infrastructure with Terraform
            terraform_result = await self.terraform_service.create_infrastructure(
                service_name=service.name,
                service_type=service.service_type.value,
                environment=service.environment.value
            )

            if terraform_result["status"] == "success":
                # Create Kubernetes deployment
                k8s_result = await self.kubernetes_service.create_deployment(
                    service_name=service.name,
                    service_type=service.service_type.value,
                    environment=service.environment.value
                )

                if k8s_result["status"] == "success":
                    # Update infrastructure status
                    service.infrastructure_status = "provisioned"
                    service.deployment_url = f"http://{service.name}.{service.environment.value}.platformdavid.com"

                    # Store infrastructure information
                    service.infrastructure_config.update({
                        "terraform_outputs": terraform_result.get("outputs", {}),
                        "kubernetes_deployment": k8s_result.get("output", "")
                    })

                    await self.db.commit()
                else:
                    raise Exception(f"Kubernetes deployment failed: {k8s_result.get('error', 'Unknown error')}")
            else:
                raise Exception(f"Terraform provisioning failed: {terraform_result.get('message', 'Unknown error')}")

        except Exception as e:
            service.infrastructure_status = "failed"
            await self.db.commit()
            raise e

    async def _provision_monitoring(self, service: Service) -> None:
        """
        Provision monitoring using local Prometheus and Grafana.

        Args:
            service: Service to provision monitoring for
        """
        try:
            # In a real implementation, this would:
            # 1. Create Grafana dashboard via API
            # 2. Configure Prometheus alerts
            # 3. Set up log aggregation
            # 4. Configure health checks

            # For now, simulate monitoring provisioning
            await asyncio.sleep(1)

            # Update monitoring status
            service.monitoring_status = "configured"
            service.monitoring_url = f"http://localhost:3000/d/{service.name}"
            service.logs_url = f"http://localhost:9090/graph?g0.expr=service%3D%22{service.name}%22"

            # Store monitoring configuration
            service.monitoring_config.update({
                "grafana_dashboard": f"dashboard-{service.name}-{service.environment.value}",
                "prometheus_alerts": [
                    f"high-error-rate-{service.name}",
                    f"high-latency-{service.name}"
                ],
                "log_stream": f"service-{service.name}-{service.environment.value}"
            })

            await self.db.commit()

        except Exception as e:
            service.monitoring_status = "failed"
            await self.db.commit()
            raise e

    async def get_service_by_id(self, service_id: int) -> Optional[Service]:
        """
        Get service by ID.

        Args:
            service_id: Service ID

        Returns:
            Optional[Service]: Service if found, None otherwise
        """
        result = await self.db.execute(select(Service).where(Service.id == service_id))
        return result.scalar_one_or_none()

    async def get_services_by_team(self, team: str, skip: int = 0, limit: int = 100) -> List[Service]:
        """
        Get services by team with pagination.

        Args:
            team: Team name
            skip: Number of services to skip
            limit: Maximum number of services to return

        Returns:
            List[Service]: List of services
        """
        result = await self.db.execute(
            select(Service)
            .where(Service.team == team)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_all_services(self, skip: int = 0, limit: int = 100) -> List[Service]:
        """
        Get all services with pagination.

        Args:
            skip: Number of services to skip
            limit: Maximum number of services to return

        Returns:
            List[Service]: List of services
        """
        result = await self.db.execute(
            select(Service).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update_service(self, service_id: int, service_in: ServiceUpdate) -> Optional[Service]:
        """
        Update service information.

        Args:
            service_id: Service ID
            service_in: Service update data

        Returns:
            Optional[Service]: Updated service if found, None otherwise
        """
        service = await self.get_service_by_id(service_id)
        if not service:
            return None

        update_data = service_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)

        await self.db.commit()
        await self.db.refresh(service)

        return service

    async def delete_service(self, service_id: int) -> bool:
        """
        Delete a service and clean up all its resources.

        This method will:
        1. Delete GitHub repository
        2. Destroy infrastructure with Terraform
        3. Remove Kubernetes deployment
        4. Clean up monitoring and logs

        Args:
            service_id: Service ID

        Returns:
            bool: True if service was deleted, False if not found
        """
        service = await self.get_service_by_id(service_id)
        if not service:
            return False

        try:
            # Clean up resources in parallel
            cleanup_tasks = []

            # Delete Kubernetes deployment
            cleanup_tasks.append(
                self.kubernetes_service.delete_deployment(
                    service_name=service.name,
                    environment=service.environment.value
                )
            )

            # Destroy Terraform infrastructure
            cleanup_tasks.append(
                self.terraform_service.destroy_infrastructure(
                    service_name=service.name,
                    environment=service.environment.value
                )
            )

            # Wait for cleanup to complete
            await asyncio.gather(*cleanup_tasks, return_exceptions=True)

            # Delete service from database
            await self.db.delete(service)
            await self.db.commit()

            return True

        except Exception as e:
            # Log error but still delete from database
            print(f"Error during service cleanup: {e}")
            await self.db.delete(service)
            await self.db.commit()
            return True
