"""
API tests for the FanDuel Platform Engineering API.

This module contains tests for the FastAPI endpoints.
"""

import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Async test client fixture."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self, client):
        """Test basic health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "FanDuel Platform Engineering API" in data["service"]
    
    def test_liveness_check(self, client):
        """Test liveness check endpoint."""
        response = client.get("/api/v1/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
    
    def test_readiness_check(self, client):
        """Test readiness check endpoint."""
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Welcome to FanDuel Platform Engineering API" in data["message"]
        assert data["version"] == "1.0.0"
        assert "/docs" in data["docs"]


class TestDeploymentEndpoints:
    """Test deployment management endpoints."""
    
    def test_create_deployment_endpoint_exists(self, client):
        """Test that create deployment endpoint exists."""
        response = client.post("/api/v1/deployments/", json={
            "name": "test-deployment",
            "team": "backend-team",
            "environment": "dev",
            "service_type": "api",
            "configuration": {
                "replicas": 3,
                "resources": {"cpu": "500m", "memory": "512Mi"}
            }
        })
        # Should return 422 for validation errors or 201 for success, not 404
        assert response.status_code in [422, 201]
    
    def test_get_deployments_endpoint_exists(self, client):
        """Test that get deployments endpoint exists."""
        response = client.get("/api/v1/deployments/")
        # Should return 200 for success, not 404
        assert response.status_code == 200
    
    def test_get_deployments_with_team_filter(self, client):
        """Test that get deployments with team filter works."""
        response = client.get("/api/v1/deployments/?team=backend-team")
        # Should return 200 for success, not 404
        assert response.status_code == 200
    
    def test_trigger_deployment_endpoint_exists(self, client):
        """Test that trigger deployment endpoint exists."""
        # First create a deployment
        create_response = client.post("/api/v1/deployments/", json={
            "name": "trigger-test",
            "team": "backend-team",
            "environment": "dev",
            "service_type": "api",
            "configuration": {"replicas": 1}
        })
        
        if create_response.status_code == 201:
            deployment_id = create_response.json()["id"]
            # Then try to trigger it
            trigger_response = client.post(f"/api/v1/deployments/{deployment_id}/trigger")
            # Should return 200 for success, not 404
            assert trigger_response.status_code == 200


class TestAPIDocumentation:
    """Test API documentation endpoints."""
    
    def test_swagger_docs(self, client):
        """Test Swagger documentation endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_docs(self, client):
        """Test ReDoc documentation endpoint."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_schema(self, client):
        """Test OpenAPI schema endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert data["info"]["title"] == "FanDuel Platform API"
        assert "paths" in data
        # Check that deployment endpoints are in the schema
        assert "/api/v1/deployments/" in data["paths"]
