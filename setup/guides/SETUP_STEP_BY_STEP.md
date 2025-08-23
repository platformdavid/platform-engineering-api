# 🚀 Step-by-Step Setup Guide

This guide will walk you through setting up the entire platform engineering project from scratch.

## **📋 Current Status**
- ✅ Code is written
- ✅ `.env` file created
- ❌ No packages installed
- ❌ No database set up
- ❌ No GitHub organization created
- ❌ No AWS infrastructure
- ❌ No Git repository initialized

## **🎯 Setup Order**
1. **Git Setup** (5 minutes)
2. **GitHub Organization** (5 minutes)
3. **Environment Configuration** (10 minutes)
4. **Package Installation** (5 minutes)
5. **Database Setup** (10 minutes)
6. **AWS Basic Setup** (15 minutes)
7. **Test the Platform** (10 minutes)

---

## **1. Git & GitHub Setup**

### **1.1 Initialize Git Repository**
```bash
# In your project root
git init
git add .
git commit -m "Initial commit: Platform Engineering API"
```

### **1.2 Create GitHub Organization**
```bash
# Go to https://github.com/organizations/new
# Organization name: platformdavid
# Plan: Free
# Description: Platform Engineering Test Organization
```

**Yes, you can create this from your `DavidKielty1` account!** This is actually better because:
- ✅ You own the organization
- ✅ You can invite others later
- ✅ You have full control
- ✅ It's free

### **1.3 Push to GitHub**
```bash
# Create repository in the platformdavid organization
# Repository name: platform-engineering-api
# Make it public (for free GitHub Actions)

# Then push
git remote add origin https://github.com/platformdavid/platform-engineering-api.git
git branch -M main
git push -u origin main
```

---

## **2. Environment Configuration**

### **2.1 Update Your `.env` File**
```bash
# Copy the template
cp env.example .env

# Edit with your actual values
nano .env
```

### **2.2 Required Environment Variables**

```env
# Application Settings
APP_NAME=Platform Engineering API
DEBUG=True
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
HOST=0.0.0.0
PORT=8000

# Database Settings (we'll set this up next)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/platform_engineering_db

# CORS Settings
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis Settings
REDIS_URL=redis://localhost:6379/0

# Logging Settings
LOG_LEVEL=INFO

# AWS Settings (we'll set this up later)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=eu-west-2
AWS_PROFILE=default
AWS_S3_BUCKET=platformdavid-platform-engineering

# GitHub Actions (we'll set this up next)
GITHUB_TOKEN=your-github-token
GITHUB_ORGANIZATION=platformdavid

# Terraform Settings
TERRAFORM_WORKSPACE_DIR=/tmp/terraform

# Local Kubernetes (we'll set this up later)
K8S_NAMESPACE=platform-engineering
K8S_CLUSTER_NAME=platformdavid-local
CONTAINER_REGISTRY_URL=ghcr.io/platformdavid

# Free Monitoring (we'll set this up later)
GRAFANA_URL=http://localhost:3000
PROMETHEUS_URL=http://localhost:9090

# SonarCloud (commented out for now)
# SONARCLOUD_TOKEN=your-sonarcloud-token
# SONARCLOUD_ORGANIZATION=platformdavid

# Platform Organization Settings
PLATFORM_ORGANIZATION=platformdavid
PLATFORM_DOMAIN=platformdavid.com

# API Keys (for external services - we'll set this up later)
EXTERNAL_API_KEY=placeholder-for-now
```

### **2.3 Generate Secret Key**
```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copy the output to SECRET_KEY in your .env
```

---

## **3. Package Installation**

### **3.1 Install Python Dependencies**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### **3.2 Verify Installation**
```bash
# Test that FastAPI works
python -c "import fastapi; print('FastAPI installed successfully')"
python -c "import sqlalchemy; print('SQLAlchemy installed successfully')"
python -c "import boto3; print('Boto3 installed successfully')"
```

---

## **4. Database Setup**

### **4.1 Install PostgreSQL**
```bash
# Option 1: Docker (recommended for testing)
docker run -d --name platform-engineering-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=platform_engineering_db -p 5432:5432 postgres:15

# Option 2: Local installation
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
```

### **4.2 Initialize Database**
```bash
# Run the database setup script
python setup_database.py
```

### **4.3 Verify Database**
```bash
# Test database connection
python -c "
from app.core.database import AsyncSessionLocal
import asyncio

async def test_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute('SELECT 1')
        print('Database connection successful!')

asyncio.run(test_db())
"
```

---

## **5. GitHub Token Setup**

### **5.1 Create GitHub Personal Access Token**
```bash
# Go to https://github.com/settings/tokens
# Click "Generate new token (classic)"
# Select scopes:
# - repo (all)
# - admin:org (all)
# - workflow
# - write:packages
# - read:packages

# Copy the token and add to your .env
GITHUB_TOKEN=ghp_your_token_here
```

### **5.2 Test GitHub Token**
```bash
# Test the token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

## **6. AWS Basic Setup**

### **6.1 Create AWS IAM User**
```bash
# Go to AWS Console → IAM → Users → Create User
# Username: platform-engineering-user
# Access type: Programmatic access

# Attach policies:
# - AmazonECS-FullAccess
# - AmazonS3FullAccess
# - AWSLambda_FullAccess
# - CloudWatchFullAccess
# - IAMFullAccess (for Terraform)

# Copy Access Key ID and Secret Access Key to your .env
```

### **6.2 Create S3 Bucket**
```bash
# Go to AWS Console → S3 → Create Bucket
# Bucket name: platformdavid-platform-engineering
# Region: eu-west-2
# Block all public access: Uncheck (for static hosting)
# Bucket versioning: Disable (to save costs)

# Update your .env
AWS_S3_BUCKET=platformdavid-platform-engineering
```

### **6.3 Create Basic VPC (if needed)**
```bash
# Go to AWS Console → VPC → Create VPC
# VPC name: platform-engineering-vpc
# CIDR: 10.0.0.0/16
# Create subnets:
# - Public: 10.0.1.0/24 (eu-west-2a)
# - Private: 10.0.2.0/24 (eu-west-2a)

# Note down subnet IDs for Terraform
```

---

## **7. Test the Platform**

### **7.1 Start the API**
```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **7.2 Test API Endpoints**
```bash
# Test health check
curl http://localhost:8000/api/v1/health

# Test services endpoint
curl http://localhost:8000/api/v1/services

# Test creating a service
curl -X POST "http://localhost:8000/api/v1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-api",
    "team": "test-team",
    "service_type": "api",
    "environment": "dev",
    "description": "Test API service"
  }'
```

### **7.3 Access API Documentation**
```bash
# Open in browser:
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

---

## **8. Optional: Local Monitoring Setup**

### **8.1 Start Prometheus & Grafana**
```bash
# Start monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access monitoring:
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

---

## **9. Troubleshooting**

### **9.1 Common Issues**

**Database Connection Error:**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check database URL
echo $DATABASE_URL
```

**GitHub Token Error:**
```bash
# Test token permissions
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/orgs/platformdavid
```

**AWS Credentials Error:**
```bash
# Test AWS credentials
aws sts get-caller-identity
```

### **9.2 Reset Everything**
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove containers
docker rm $(docker ps -aq)

# Reset database
docker run --rm -v $(pwd):/app postgres:15 psql -h localhost -U postgres -d platform_engineering_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

---

## **10. Next Steps**

Once everything is working:

1. **Test Service Creation:**
   ```bash
   # Create a service from template
   curl -X POST "http://localhost:8000/api/v1/services/from-template/fastapi-api" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-first-service",
       "team": "my-team",
       "environment": "dev",
       "description": "My first platform engineering service"
     }'
   ```

2. **Test Provisioning:**
   ```bash
   # Provision the service
   curl -X POST "http://localhost:8000/api/v1/services/1/provision" \
     -H "Content-Type: application/json" \
     -d '{
       "provision_cicd": true,
       "provision_infrastructure": true,
       "provision_monitoring": true
     }'
   ```

3. **Explore the Platform:**
   - Check GitHub for created repositories
   - Check AWS for created resources
   - Check monitoring dashboards

---

## **🎉 Success Checklist**

- ✅ Git repository initialized and pushed
- ✅ GitHub organization created
- ✅ Environment variables configured
- ✅ Python packages installed
- ✅ Database running and initialized
- ✅ GitHub token working
- ✅ AWS credentials configured
- ✅ S3 bucket created
- ✅ API server running
- ✅ Health check passing
- ✅ Service creation working

**You're ready to demonstrate your platform engineering skills!** 🚀
