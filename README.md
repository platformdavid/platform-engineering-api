# Platform Engineering API

A comprehensive platform engineering API for managing services, CI/CD pipelines, and infrastructure. Built with FastAPI, designed for platform engineering teams

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
python -m uvicorn setup.test_api:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## 📁 Project Structure

```
FanDuel/
├── app/                    # Main application code
│   ├── api/               # API endpoints
│   ├── core/              # Core functionality
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   └── services/          # Business logic
├── setup/                 # Setup scripts and documentation
│   ├── install.py         # Installation script
│   ├── test_api.py        # Test suite and API server
│   ├── setup_database.py  # Database initialization
│   ├── env.example        # Environment template
│   └── *.md              # Setup documentation
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
├── Dockerfile            # Docker image
└── README.md             # This file
```

## 🎯 Features

### **Core Platform Features**
- ✅ **Service Management**: Create and manage services from templates
- ✅ **CI/CD Automation**: GitHub Actions integration
- ✅ **Infrastructure as Code**: Terraform integration
- ✅ **Monitoring**: Prometheus and Grafana integration
- ✅ **Multi-Environment Support**: Dev, staging, production
- ✅ **Team Management**: Multi-team service organization

### **Service Templates**
- **FastAPI API**: Python REST API with comprehensive testing
- **React Web**: Frontend application with modern tooling
- **Celery Worker**: Background task processing
- **Node.js API**: Express.js REST API

### **Platform Tools Integration**
- **AWS**: ECS, S3, Lambda, CloudWatch
- **Kubernetes**: Local and cloud deployments
- **GitHub**: Repository management and CI/CD
- **Monitoring**: Prometheus, Grafana, health checks

## 🛠️ Setup Options

### **Option 1: Simple Setup (Recommended)**
```bash
python setup/install.py
python setup/test_api.py
python -m uvicorn setup.test_api:app --reload
```

### **Option 2: Full Setup with Database**
See `setup/SETUP_GUIDE.md` for complete instructions.

### **Option 3: Free Tier Setup**
See `setup/FREE_TIER_SETUP.md` for zero-cost setup.

### **Option 4: Cost-Optimized Setup**
See `setup/COST_OPTIMIZATION_GUIDE.md` for cost optimization.

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
- AWS credentials (for infrastructure)
- GitHub token (for CI/CD)
- Database connection (optional)
- Kubernetes cluster (optional)

## 🧪 Testing

### **Run Tests**
```bash
# Test the installation
python setup/test_api.py

# Run application tests
pytest

# Run with coverage
pytest --cov=app
```

### **API Testing**
```bash
# Start the API
python -m uvicorn setup.test_api:app --reload

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/services
```

## 🚀 Deployment

### **Development**
```bash
python -m uvicorn setup.test_api:app --reload
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
- `GET /` - Root endpoint with API information
- `GET /health` - Health check for all components
- `GET /services` - List managed services
- `GET /platform-tools` - Platform tools information
- `GET /config` - Current configuration

### **Service Management**
- `POST /api/v1/services` - Create new service
- `GET /api/v1/services` - List all services
- `GET /api/v1/services/{id}` - Get service details
- `PUT /api/v1/services/{id}` - Update service
- `DELETE /api/v1/services/{id}` - Delete service

### **Service Provisioning**
- `POST /api/v1/services/{id}/provision` - Provision service
- `POST /api/v1/services/from-template/{template}` - Create from template

## 🎯 Use Cases

### **Platform Engineering Teams**
- Self-service service creation
- Standardized CI/CD pipelines
- Infrastructure automation
- Multi-team support

### **Development Teams**
- Quick service setup
- Automated testing
- Deployment automation
- Monitoring integration

### **DevOps Teams**
- Infrastructure as Code
- Cost optimization
- Security compliance
- Performance monitoring

## 🔒 Security

- Environment-based configuration
- Secure secret management
- API authentication (configurable)
- CORS protection
- Input validation with Pydantic

## 📈 Monitoring

- Health checks for all components
- Prometheus metrics
- Grafana dashboards
- AWS CloudWatch integration
- Custom alerting

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
