"""
BuildKite service for CI/CD pipeline management.

This service integrates with BuildKite API to create and manage CI/CD pipelines.
"""

import httpx
from typing import Dict, Any, List, Optional
import asyncio

from app.config import settings


class BuildKiteService:
    """
    Service for managing BuildKite CI/CD pipelines.
    
    BuildKite is a self-hosted CI/CD platform used by companies like
    FanDuel, Netflix, and Spotify for secure, scalable CI/CD.
    """
    
    def __init__(self):
        """Initialize BuildKite service with API credentials."""
        self.api_token = settings.buildkite_api_token
        self.organization = settings.buildkite_organization
        self.base_url = "https://api.buildkite.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    async def create_pipeline(self, service_name: str, team: str, service_type: str, pipeline_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new BuildKite pipeline for a service.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service (api, web, worker)
            pipeline_config: Optional custom pipeline configuration
            
        Returns:
            Dict containing pipeline information
        """
        # Use custom config or generate default
        if pipeline_config:
            config = pipeline_config
        else:
            config = self._generate_pipeline_config(service_name, team, service_type)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/organizations/{self.organization}/pipelines",
                headers=self.headers,
                json=config
            )
            response.raise_for_status()
            return response.json()
    
    async def trigger_build(self, pipeline_slug: str, branch: str = "main") -> Dict[str, Any]:
        """
        Trigger a new build for a pipeline.
        
        Args:
            pipeline_slug: Pipeline identifier
            branch: Branch to build from
            
        Returns:
            Dict containing build information
        """
        build_data = {
            "branch": branch,
            "message": f"Platform Engineering: Automated build for {pipeline_slug}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/organizations/{self.organization}/pipelines/{pipeline_slug}/builds",
                headers=self.headers,
                json=build_data
            )
            response.raise_for_status()
            return response.json()
    
    async def get_pipeline_status(self, pipeline_slug: str) -> Dict[str, Any]:
        """
        Get the current status of a pipeline.
        
        Args:
            pipeline_slug: Pipeline identifier
            
        Returns:
            Dict containing pipeline status
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/organizations/{self.organization}/pipelines/{pipeline_slug}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    def _generate_pipeline_config(self, service_name: str, team: str, service_type: str) -> Dict[str, Any]:
        """
        Generate BuildKite pipeline configuration with comprehensive testing.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service
            
        Returns:
            Pipeline configuration dictionary
        """
        # Base pipeline configuration
        config = {
            "name": service_name,
            "repository": f"git@github.com:platformdavid/{service_name}.git",
            "steps": [],
            "env": {
                "SERVICE_NAME": service_name,
                "TEAM": team,
                "SERVICE_TYPE": service_type,
                "SONARQUBE_TOKEN": "${SONARQUBE_TOKEN}",
                "DOCKER_REGISTRY": "registry.platformdavid.com"
            }
        }
        
        # Common testing steps for all service types
        common_test_steps = [
            {
                "type": "script",
                "name": "🔍 Lint & Format Check",
                "command": "make lint format-check"
            },
            {
                "type": "script",
                "name": "🧪 Run Unit Tests",
                "command": "make test"
            },
            {
                "type": "script",
                "name": "📊 SonarQube Analysis",
                "command": "make sonarqube"
            }
        ]
        
        # Add steps based on service type
        if service_type == "api":
            config["steps"] = [
                # Common testing steps
                *common_test_steps,
                
                # API-specific steps
                {
                    "type": "script",
                    "name": "🔒 Security Scan",
                    "command": "make security-scan"
                },
                {
                    "type": "script",
                    "name": "🐳 Build Docker Image",
                    "command": "docker build -t platformdavid/$SERVICE_NAME:$BUILDKITE_COMMIT ."
                },
                {
                    "type": "script",
                    "name": "🧪 Integration Tests",
                    "command": "make integration-tests"
                },
                {
                    "type": "script",
                    "name": "🚀 Deploy to Kubernetes",
                    "command": "kubectl apply -f k8s/ && kubectl rollout status deployment/$SERVICE_NAME"
                },
                {
                    "type": "script",
                    "name": "💨 Smoke Tests",
                    "command": "make smoke-tests"
                },
                {
                    "type": "script",
                    "name": "❤️ Health Check",
                    "command": "make health-check"
                }
            ]
        elif service_type == "web":
            config["steps"] = [
                # Common testing steps
                *common_test_steps,
                
                # Web-specific steps
                {
                    "type": "script",
                    "name": "📦 Install Dependencies",
                    "command": "npm ci"
                },
                {
                    "type": "script",
                    "name": "🧪 Frontend Tests",
                    "command": "npm run test:unit"
                },
                {
                    "type": "script",
                    "name": "🎨 Visual Regression Tests",
                    "command": "npm run test:visual"
                },
                {
                    "type": "script",
                    "name": "🏗️ Build Application",
                    "command": "npm run build"
                },
                {
                    "type": "script",
                    "name": "🚀 Deploy to CDN",
                    "command": "aws s3 sync dist/ s3://platformdavid-web-assets/$SERVICE_NAME/"
                },
                {
                    "type": "script",
                    "name": "💨 Smoke Tests",
                    "command": "make smoke-tests"
                },
                {
                    "type": "script",
                    "name": "❤️ Health Check",
                    "command": "make health-check"
                }
            ]
        elif service_type == "worker":
            config["steps"] = [
                # Common testing steps
                *common_test_steps,
                
                # Worker-specific steps
                {
                    "type": "script",
                    "name": "🔒 Security Scan",
                    "command": "make security-scan"
                },
                {
                    "type": "script",
                    "name": "🐳 Build Worker Image",
                    "command": "docker build -t platformdavid/$SERVICE_NAME-worker:$BUILDKITE_COMMIT ."
                },
                {
                    "type": "script",
                    "name": "🧪 Worker Tests",
                    "command": "make worker-tests"
                },
                {
                    "type": "script",
                    "name": "🚀 Deploy Worker",
                    "command": "kubectl apply -f k8s/worker.yaml && kubectl rollout status deployment/$SERVICE_NAME-worker"
                },
                {
                    "type": "script",
                    "name": "💨 Smoke Tests",
                    "command": "make smoke-tests"
                }
            ]
        
        return config
    
    def generate_custom_pipeline_config(self, service_name: str, team: str, service_type: str, 
                                      enable_linting: bool = True,
                                      enable_formatting: bool = True,
                                      enable_unit_tests: bool = True,
                                      enable_integration_tests: bool = True,
                                      enable_sonarqube: bool = True,
                                      enable_security_scan: bool = True,
                                      enable_smoke_tests: bool = True,
                                      enable_health_check: bool = True,
                                      enable_visual_tests: bool = False) -> Dict[str, Any]:
        """
        Generate custom pipeline configuration based on team preferences.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service
            enable_linting: Enable linting checks
            enable_formatting: Enable formatting checks
            enable_unit_tests: Enable unit tests
            enable_integration_tests: Enable integration tests
            enable_sonarqube: Enable SonarQube analysis
            enable_security_scan: Enable security scanning
            enable_smoke_tests: Enable smoke tests
            enable_health_check: Enable health checks
            enable_visual_tests: Enable visual regression tests (web only)
            
        Returns:
            Custom pipeline configuration
        """
        config = {
            "name": service_name,
            "repository": f"git@github.com:platformdavid/{service_name}.git",
            "steps": [],
            "env": {
                "SERVICE_NAME": service_name,
                "TEAM": team,
                "SERVICE_TYPE": service_type,
                "SONARQUBE_TOKEN": "${SONARQUBE_TOKEN}",
                "DOCKER_REGISTRY": "registry.platformdavid.com"
            }
        }
        
        steps = []
        
        # Add conditional steps based on preferences
        if enable_linting:
            steps.append({
                "type": "script",
                "name": "🔍 Lint Check",
                "command": "make lint"
            })
        
        if enable_formatting:
            steps.append({
                "type": "script",
                "name": "🎨 Format Check",
                "command": "make format-check"
            })
        
        if enable_unit_tests:
            steps.append({
                "type": "script",
                "name": "🧪 Unit Tests",
                "command": "make test"
            })
        
        if enable_sonarqube:
            steps.append({
                "type": "script",
                "name": "📊 SonarQube Analysis",
                "command": "make sonarqube"
            })
        
        if enable_security_scan:
            steps.append({
                "type": "script",
                "name": "🔒 Security Scan",
                "command": "make security-scan"
            })
        
        # Service-specific steps
        if service_type == "api":
            if enable_integration_tests:
                steps.append({
                    "type": "script",
                    "name": "🧪 Integration Tests",
                    "command": "make integration-tests"
                })
            
            steps.extend([
                {
                    "type": "script",
                    "name": "🐳 Build Docker Image",
                    "command": "docker build -t platformdavid/$SERVICE_NAME:$BUILDKITE_COMMIT ."
                },
                {
                    "type": "script",
                    "name": "🚀 Deploy to Kubernetes",
                    "command": "kubectl apply -f k8s/ && kubectl rollout status deployment/$SERVICE_NAME"
                }
            ])
            
        elif service_type == "web":
            steps.extend([
                {
                    "type": "script",
                    "name": "📦 Install Dependencies",
                    "command": "npm ci"
                },
                {
                    "type": "script",
                    "name": "🏗️ Build Application",
                    "command": "npm run build"
                }
            ])
            
            if enable_visual_tests:
                steps.append({
                    "type": "script",
                    "name": "🎨 Visual Regression Tests",
                    "command": "npm run test:visual"
                })
            
            steps.append({
                "type": "script",
                "name": "🚀 Deploy to CDN",
                "command": "aws s3 sync dist/ s3://platformdavid-web-assets/$SERVICE_NAME/"
            })
            
        elif service_type == "worker":
            steps.extend([
                {
                    "type": "script",
                    "name": "🐳 Build Worker Image",
                    "command": "docker build -t platformdavid/$SERVICE_NAME-worker:$BUILDKITE_COMMIT ."
                },
                {
                    "type": "script",
                    "name": "🚀 Deploy Worker",
                    "command": "kubectl apply -f k8s/worker.yaml && kubectl rollout status deployment/$SERVICE_NAME-worker"
                }
            ])
        
        # Post-deployment tests
        if enable_smoke_tests:
            steps.append({
                "type": "script",
                "name": "💨 Smoke Tests",
                "command": "make smoke-tests"
            })
        
        if enable_health_check:
            steps.append({
                "type": "script",
                "name": "❤️ Health Check",
                "command": "make health-check"
            })
        
        config["steps"] = steps
        return config
