# FanDuel Platform Engineering API

A comprehensive platform engineering API for managing services, CI/CD pipelines, and infrastructure. Built with FastAPI, designed for enterprise platform engineering teams.

## 🎉 **Success Story**

This platform has been successfully tested and proven to work end-to-end:
- ✅ **Complete CI/CD Pipeline**: GitHub Actions with automated testing, security scanning, and validation
- ✅ **Service Provisioning**: Automated repository creation with all necessary files
- ✅ **Infrastructure Ready**: Kubernetes manifests, Docker configurations, and monitoring setup
- ✅ **Enterprise Grade**: Repository pattern, proper error handling, and scalable architecture

## 🚀 Quick Start

### **1. Install Dependencies**
```bash
python setup/install.py
```

### **2. Test Installation**
```bash
python setup/test_api.py
```

### **3. Run the API**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Visit http://localhost:8080/docs for interactive API documentation.

## 📁 Project Structure

```
FanDuel/
├── app/                    # Main application code
│   ├── api/               # API endpoints and routing
│   │   └── v1/
│   │       ├── endpoints/ # Service, health, infrastructure endpoints
│   │       └── api.py     # Main API router
│   ├── core/              # Core functionality (database, config)
│   ├── models/            # SQLAlchemy database models
│   ├── schemas/           # Pydantic schemas and DTOs
│   ├── services/          # Business logic services
│   │   ├── github_actions_service.py    # CI/CD pipeline management
│   │   ├── repository_file_service.py   # Repository file generation
│   │   ├── platform_service.py          # Main orchestration
│   │   ├── terraform_service.py         # Infrastructure as Code
│   │   └── infrastructure_service.py    # Background infrastructure tasks
│   └── repositories/      # Repository pattern implementation
├── setup/                 # Setup scripts and documentation
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image
└── README.md             # This file
```

## 🎯 Features

### **✅ Proven Platform Features**
- **Service Management**: Create and manage services with full lifecycle
- **CI/CD Automation**: GitHub Actions with comprehensive testing pipeline
- **Repository Generation**: Complete repository setup with all necessary files
- **Infrastructure as Code**: Terraform integration for AWS resources
- **Monitoring Integration**: Prometheus and Grafana ready
- **Multi-Environment Support**: Dev, staging, production environments
- **Team Management**: Multi-team service organization

### **✅ Working Service Templates**
- **FastAPI API**: Python REST API with comprehensive testing suite
- **Complete CI/CD**: GitHub Actions workflow with test, security, build, and validation
- **Kubernetes Ready**: Deployment and service manifests
- **Docker Support**: Containerization with proper configurations

### **✅ Platform Tools Integration**
- **AWS**: ECS, S3, Lambda, CloudWatch integration
- **Kubernetes**: Local and cloud deployments
- **GitHub**: Repository management and CI/CD automation
- **Monitoring**: Prometheus, Grafana, health checks

## 🏗️ Architecture

### **Two-Step Service Creation Process**
1. **Create Service** (`POST /api/v1/services/`): Creates database record
2. **Provision Service** (`POST /api/v1/services/{id}/provision`): Creates GitHub repo, CI/CD, infrastructure

### **Repository Pattern**
- **BaseRepository**: Generic repository implementation
- **ServiceRepository**: Service-specific database operations
- **ServiceMapper**: DTO to entity mapping

### **Background Tasks**
- **InfrastructureService**: Handles long-running Terraform operations
- **Async Processing**: Non-blocking API responses

## 🛠️ Setup Options

### **Option 1: Simple Setup (Recommended)**
```bash
python setup/install.py
python setup/test_api.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **Option 2: Full Setup with Database**
See `setup/SETUP_GUIDE.md` for complete instructions.

### **Option 3: Free Tier Setup**
See `setup/FREE_TIER_SETUP.md` for zero-cost setup.

## 📚 Documentation

All setup documentation is organized in the `setup/` folder:

- **`setup/README.md`** - Setup folder overview
- **`setup/SETUP_GUIDE.md`** - Main setup guide
- **`setup/SETUP_STEP_BY_STEP.md`** - Detailed instructions
- **`setup/FREE_TIER_SETUP.md`** - Free setup guide
- **`setup/COST_OPTIMIZATION_GUIDE.md`** - Cost optimization

## 🔧 Configuration

### **Environment Variables**
```bash
# Copy the template
cp setup/env.example .env

# Edit with your values
nano .env
```

### **Required Configuration**
- **GitHub Token**: For repository creation and CI/CD (with `repo` and `delete_repo` scopes)
- **AWS Credentials**: For infrastructure provisioning
- **Database Connection**: SQLite by default (PostgreSQL optional)

## 🧪 Testing

### **API Testing**
```bash
# Start the API
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

# Test endpoints
curl http://localhost:8080/api/v1/health
curl http://localhost:8080/api/v1/services/
```

### **Service Creation Test**
```bash
# Create a service
curl -X POST "http://localhost:8080/api/v1/services/" \
  -H "Content-Type: application/json" \
  -d '{"name": "test-service", "description": "Test service", "service_type": "api", "team": "test-team", "environment": "staging"}'

# Provision the service
curl -X POST "http://localhost:8080/api/v1/services/{id}/provision" \
  -H "Content-Type: application/json" \
  -d '{"provision_cicd": true, "provision_infrastructure": true, "provision_monitoring": true}'
```

## 🚀 Deployment

### **Development**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

### **Production**
```bash
# Using Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app

# Using Docker
docker-compose up --build
```

## 📊 API Endpoints

### **Core Endpoints**
- `GET /api/v1/health` - Health check for all components
- `GET /api/v1/services/` - List all managed services
- `GET /api/v1/services/{id}` - Get service details

### **Service Management**
- `POST /api/v1/services/` - Create new service
- `PUT /api/v1/services/{id}` - Update service
- `DELETE /api/v1/services/{id}` - Delete service

### **Service Provisioning**
- `POST /api/v1/services/{id}/provision` - Provision service (GitHub repo + CI/CD + infrastructure)

### **Infrastructure Management**
- `POST /api/v1/infrastructure/provision` - Provision infrastructure
- `POST /api/v1/infrastructure/destroy` - Destroy infrastructure
- `GET /api/v1/infrastructure/operations` - List infrastructure operations

## 🎯 Use Cases

### **Platform Engineering Teams**
- Self-service service creation with standardized templates
- Automated CI/CD pipeline generation
- Infrastructure as Code automation
- Multi-team service management

### **Development Teams**
- Quick service setup with best practices
- Automated testing and security scanning
- Deployment automation
- Monitoring integration

### **DevOps Teams**
- Infrastructure as Code with Terraform
- Cost optimization and resource management
- Security compliance automation
- Performance monitoring and alerting

## 🔒 Security

- Environment-based configuration management
- Secure secret management with GitHub tokens
- API input validation with Pydantic schemas
- CORS protection
- Repository pattern for data access

## 📈 Monitoring

- Health checks for all components
- Prometheus metrics integration
- Grafana dashboard templates
- AWS CloudWatch integration
- Custom alerting and notifications

## 🧹 Repository Cleanup

The platform includes tools for managing test repositories:

```bash
# Clean up test repositories (preserves important ones)
python cleanup_repos.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For setup issues, see the documentation in the `setup/` folder.

For technical issues:
1. Check the troubleshooting guides
2. Review the API documentation
3. Check the test suite
4. Open an issue on GitHub

---

**Built with ❤️ for Platform Engineering teams**

*Successfully tested and proven to work in production environments*
