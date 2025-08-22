# Platform Engineering API - Setup Guide

## Overview

This guide will help you set up the Platform Engineering API on your system. The API provides endpoints for managing services, CI/CD pipelines, and infrastructure.

## Prerequisites

- Python 3.11+ (3.13 recommended)
- pip (Python package installer)
- Virtual environment (recommended)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd FanDuel
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python install.py
```

This script will:
- Install all required packages with proper version compatibility
- Handle Python 3.13 compatibility issues
- Verify the installation
- Provide detailed error reporting

### 4. Test the Installation

```bash
python test_api.py
```

You should see all tests pass with ✅ marks.

### 5. Run the API

```bash
python -m uvicorn test_api:app --reload
```

The API will be available at:
- Main API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API information
- `GET /health` - Health check for all components
- `GET /services` - List of managed services
- `GET /platform-tools` - Information about platform tools
- `GET /config` - Current configuration

### Example Usage

```bash
# Health check
curl http://localhost:8000/health

# List services
curl http://localhost:8000/services

# Get platform tools info
curl http://localhost:8000/platform-tools
```

## Troubleshooting

### Common Issues

#### 1. Pydantic/FastAPI Compatibility Issues

**Symptoms**: `ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'`

**Solution**: 
```bash
# Run the installation script which handles this automatically
python install.py
```

#### 2. Database Package Installation Failures

**Symptoms**: Compilation errors with `psycopg2-binary`, `asyncpg`, or `sqlalchemy`

**Solution**: 
- The installation script skips problematic database packages
- Consider using Python 3.11 or 3.12 instead of 3.13
- Install database packages manually later if needed

#### 3. Rust Compilation Issues

**Symptoms**: Errors about missing Rust or Cargo

**Solution**:
- The installation script uses `--only-binary=all` for packages that require compilation
- Install Rust from https://rustup.rs/ if you need to compile packages manually

### Python Version Compatibility

| Python Version | Status | Notes |
|----------------|--------|-------|
| 3.11 | ✅ Full Support | All packages work |
| 3.12 | ✅ Full Support | All packages work |
| 3.13 | ⚠️ Limited Support | Some packages may need manual installation |

### Package Compatibility Matrix

| Package | Python 3.11 | Python 3.12 | Python 3.13 |
|---------|-------------|-------------|-------------|
| FastAPI | ✅ | ✅ | ✅ |
| Pydantic | ✅ | ✅ | ✅ |
| SQLAlchemy | ✅ | ✅ | ⚠️ Manual |
| psycopg2-binary | ✅ | ✅ | ❌ |
| asyncpg | ✅ | ✅ | ❌ |
| Celery | ✅ | ✅ | ⚠️ Manual |
| Redis | ✅ | ✅ | ⚠️ Manual |

## Development Setup

### Code Quality Tools

The project includes several code quality tools:

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Type checking
mypy .
```

### Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Settings
APP_NAME=Platform Engineering API
DEBUG=true
SECRET_KEY=your-secret-key

# Database (optional)
DATABASE_URL=sqlite:///./app.db

# AWS Settings
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=eu-west-2

# GitHub Settings
GITHUB_TOKEN=your-github-token
GITHUB_ORGANIZATION=your-org

# Kubernetes Settings
K8S_NAMESPACE=platform-engineering
```

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Using Docker

```bash
# Build image
docker build -t platform-engineering-api .

# Run container
docker run -p 8000:8000 platform-engineering-api
```

## File Structure

After installation, your project structure will include:

```
FanDuel/
├── install.py              # Installation script
├── test_api.py             # Test suite and API server
├── requirements.txt        # Package requirements
├── SETUP_GUIDE.md         # This guide
├── app/                   # Main application code
├── tests/                 # Test files
└── venv/                  # Virtual environment
```

## Next Steps

1. **Configure your environment**: Set up AWS credentials, GitHub tokens, etc.
2. **Add database support**: Install and configure PostgreSQL if needed
3. **Set up monitoring**: Configure Prometheus and Grafana
4. **Deploy to production**: Use Docker or your preferred deployment method
5. **Add custom services**: Extend the API with your specific platform needs

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Python version compatibility
3. Run the installation script again
4. Check the project issues on GitHub

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Note**: This API is designed for platform engineering teams to manage their infrastructure, CI/CD pipelines, and services. It provides a unified interface for common platform operations.
