# 🚀 Platform Engineering API Setup Guide

This guide will help you set up the complete Platform Engineering API with all necessary tools and configurations.

## 📋 Prerequisites

Before starting, ensure you have:
- Python 3.11+
- Docker and Docker Compose
- Git
- AWS CLI configured
- PostgreSQL (or use Docker)

## 🔧 Initial Setup

### 1. Clone and Setup Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd platform-engineering-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env with your actual values
nano .env
```

**Required Environment Variables:**

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/platform_engineering_db

# AWS Configuration (for Terraform)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
AWS_PROFILE=default

# BuildKite (Self-hosted CI/CD)
BUILDKITE_API_TOKEN=your-buildkite-api-token
BUILDKITE_ORGANIZATION=platformdavid

# GitHub (for repository management)
GITHUB_TOKEN=your-github-token
GITHUB_ORGANIZATION=platformdavid

# SonarQube (Code quality)
SONARQUBE_TOKEN=your-sonarqube-token
SONARQUBE_URL=https://sonarqube.platformdavid.com

# Kubernetes
K8S_NAMESPACE=platform-engineering
K8S_CLUSTER_NAME=platformdavid-cluster
```

### 3. Database Setup

```bash
# Initialize database with sample data
python setup_database.py
```

This creates:
- Service templates (fastapi-api, react-web, celery-worker, nodejs-api)
- Sample services (user-service, frontend-app, email-worker)
- Platform configuration

## 🛠️ Tool Setup

### AWS Configuration

```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure

# Test AWS access
aws sts get-caller-identity
```

### BuildKite Setup

BuildKite is a **self-hosted CI/CD platform**. You'll need to:

1. **Install BuildKite Agent** on your build servers
2. **Set up BuildKite Server** (or use BuildKite Cloud)
3. **Get API Token** from BuildKite dashboard

```bash
# Example BuildKite agent setup
curl -Lfs https://github.com/buildkite/agent/releases/latest/download/buildkite-agent-linux-amd64 -o /usr/local/bin/buildkite-agent
chmod +x /usr/local/bin/buildkite-agent

# Configure agent
buildkite-agent start --token "your-agent-token"
```

### SonarQube Setup

SonarQube provides code quality analysis:

1. **Install SonarQube** (Docker recommended)
2. **Create project** in SonarQube
3. **Get API token**

```bash
# Run SonarQube with Docker
docker run -d --name sonarqube \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:latest
```

### GitHub Repository Setup

```bash
# Create GitHub organization (if needed)
# Go to github.com and create organization: platformdavid

# Create personal access token
# Go to GitHub Settings > Developer settings > Personal access tokens
# Generate token with repo, admin:org permissions
```

### Kubernetes Setup

```bash
# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Configure kubectl for your cluster
kubectl config set-cluster platformdavid-cluster --server=https://your-cluster-endpoint
kubectl config set-credentials platformdavid-user --token=your-token
kubectl config set-context platformdavid-context --cluster=platformdavid-cluster --user=platformdavid-user
kubectl config use-context platformdavid-context
```

## 🚀 Running the Application

### Development Mode

```bash
# Start the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Visit API documentation
open http://localhost:8000/docs
```

### Production Mode

```bash
# Using Docker Compose
docker-compose up --build

# Or using Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🧪 Testing the Platform

### 1. Create a Service from Template

```bash
curl -X POST "http://localhost:8000/api/v1/services/from-template/fastapi-api" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-api",
    "team": "test-team",
    "environment": "dev",
    "description": "Test API service"
  }'
```

### 2. Provision the Service

```bash
curl -X POST "http://localhost:8000/api/v1/services/1/provision" \
  -H "Content-Type: application/json" \
  -d '{
    "provision_cicd": true,
    "provision_infrastructure": true,
    "provision_monitoring": true
  }'
```

### 3. Check Service Status

```bash
curl "http://localhost:8000/api/v1/services/1"
```

## 📊 CI/CD Pipeline Features

### Comprehensive Testing Stages

The platform includes these testing stages:

**Common for All Services:**
- ✅ **Linting** (flake8, eslint, etc.)
- ✅ **Formatting** (black, prettier, etc.)
- ✅ **Unit Tests** (pytest, jest, etc.)
- ✅ **SonarQube Analysis** (code quality)

**API Services:**
- ✅ **Security Scan** (bandit, safety, etc.)
- ✅ **Integration Tests** (API testing)
- ✅ **Smoke Tests** (basic functionality)
- ✅ **Health Check** (service health)

**Web Services:**
- ✅ **Frontend Tests** (unit tests)
- ✅ **Visual Regression Tests** (optional)
- ✅ **Smoke Tests** (page loading)
- ✅ **Health Check** (CDN health)

**Worker Services:**
- ✅ **Security Scan** (vulnerability scanning)
- ✅ **Worker Tests** (task processing)
- ✅ **Smoke Tests** (queue health)

### Configurable Pipeline Options

Teams can customize their pipelines:

```bash
# Create custom pipeline configuration
curl -X POST "http://localhost:8000/api/v1/services/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "custom-api",
    "team": "backend-team",
    "service_type": "api",
    "environment": "staging",
    "configuration": {
      "enable_linting": true,
      "enable_formatting": true,
      "enable_unit_tests": true,
      "enable_integration_tests": false,
      "enable_sonarqube": true,
      "enable_security_scan": true,
      "enable_smoke_tests": true,
      "enable_health_check": true
    }
  }'
```

## 🔍 Why Different Tests for Different Service Types?

### API Services (Backend)
- **More Integration Tests**: APIs need to test database connections, external services
- **Security Focus**: Backend APIs handle sensitive data
- **Performance Tests**: API response times are critical

### Web Services (Frontend)
- **Visual Tests**: Frontend needs visual regression testing
- **Browser Tests**: Different browsers, devices
- **Performance Tests**: Page load times, bundle sizes

### Worker Services
- **Queue Tests**: Message processing, retry logic
- **Resource Tests**: Memory usage, CPU utilization
- **Reliability Tests**: Long-running processes

## 📁 Pipeline Configuration Files

When you create a pipeline, the platform generates:

1. **BuildKite Pipeline Config** (stored in BuildKite)
2. **Terraform Files** (infrastructure as code)
3. **Kubernetes Manifests** (deployment configs)
4. **Makefile** (local development commands)

These are **not stored in your local repo** - they're managed by the platform engineering API and applied to the respective tools.

## 🗄️ Database Schema

The database includes:

```sql
-- Services table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    team VARCHAR NOT NULL,
    service_type VARCHAR NOT NULL,
    environment VARCHAR NOT NULL,
    configuration JSONB NOT NULL,
    infrastructure_config JSONB NOT NULL,
    monitoring_config JSONB NOT NULL,
    status VARCHAR DEFAULT 'pending',
    cicd_status VARCHAR DEFAULT 'not_configured',
    infrastructure_status VARCHAR DEFAULT 'not_provisioned',
    monitoring_status VARCHAR DEFAULT 'not_configured',
    repository_url VARCHAR,
    deployment_url VARCHAR,
    monitoring_url VARCHAR,
    logs_url VARCHAR,
    description TEXT,
    tags JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check PostgreSQL is running
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -U user -d platform_engineering_db
   ```

2. **AWS Credentials Not Found**
   ```bash
   # Check AWS configuration
   aws sts get-caller-identity
   
   # Set environment variables
   export AWS_ACCESS_KEY_ID=your-key
   export AWS_SECRET_ACCESS_KEY=your-secret
   ```

3. **BuildKite API Token Invalid**
   ```bash
   # Test BuildKite connection
   curl -H "Authorization: Bearer $BUILDKITE_API_TOKEN" \
     https://api.buildkite.com/v2/user
   ```

4. **Kubernetes Connection Failed**
   ```bash
   # Test kubectl connection
   kubectl get nodes
   
   # Check cluster context
   kubectl config current-context
   ```

## 📚 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create Services**: Use the templates to create new services
3. **Customize Pipelines**: Modify testing stages based on team needs
4. **Scale Infrastructure**: Add more AWS resources, Kubernetes clusters
5. **Monitor Services**: Set up Grafana dashboards, Prometheus alerts

## 🆘 Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify environment variables: `env | grep PLATFORM`
3. Test individual components: AWS, BuildKite, Kubernetes
4. Review the API documentation: `/docs` endpoint

---

**🎉 Congratulations!** You now have a complete Platform Engineering API that can orchestrate CI/CD, infrastructure, and monitoring for multiple teams.
