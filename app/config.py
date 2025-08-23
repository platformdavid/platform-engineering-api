"""
Application configuration settings.

This module contains all configuration settings for the Platform Engineering API.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Settings
    app_name: str = "Platform Engineering API"
    debug: bool = True
    secret_key: str = "your-secret-key-here-change-in-production"
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database Settings
    database_url: str = "sqlite+aiosqlite:///./platform_engineering.db"
    
    # CORS Settings
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins to list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    # Redis Settings
    redis_url: str = "redis://localhost:6379/0"
    
    # Logging Settings
    log_level: str = "INFO"
    
    # AWS Settings
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "eu-west-2"
    aws_profile: str = "default"
    aws_s3_bucket: str = ""
    
    # VPC Settings
    vpc_id: str = ""
    public_subnet_id: str = ""
    private_subnet_id: str = ""
    
    # GitHub Actions Settings
    github_token: str = ""
    github_organization: str = "platformdavid"
    
    # Terraform Settings
    terraform_workspace_dir: str = "/tmp/terraform"
    
    # Kubernetes Settings
    k8s_namespace: str = "platform-engineering"
    k8s_cluster_name: str = "platformdavid-local"
    container_registry_url: str = "ghcr.io/platformdavid"
    
    # Monitoring Settings
    grafana_url: str = "http://localhost:3000"
    prometheus_url: str = "http://localhost:9090"
    
    # SonarCloud Settings (commented out for now)
    # sonarcloud_token: Optional[str] = None
    # sonarcloud_organization: str = "platformdavid"
    
    # Platform Organization Settings
    platform_organization: str = "platformdavid"
    platform_domain: str = "platformdavid.com"
    
    # External API Settings
    external_api_key: str = "your-external-api-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()
