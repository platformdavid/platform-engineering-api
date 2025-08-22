# FanDuel Platform Engineering API

A modern FastAPI-based platform engineering template designed for the FanDuel Builder Tools team.

## 🚀 Features

- **FastAPI** with modern async Python
- **SQLAlchemy** with async database operations
- **Pydantic** for data validation and serialization
- **Automatic API Documentation** with OpenAPI/Swagger
- **Testing** with pytest-asyncio and httpx
- **Code Quality** with black, flake8, isort, and mypy
- **Docker** support for containerization
- **Environment Management** with pydantic-settings
- **Task Queue** with Celery and Redis

## 🏗️ Architecture

This template follows modern platform engineering practices:

- **Clean Architecture** with separation of concerns
- **Service Layer** for business logic
- **Dependency Injection** ready
- **Type Hints** throughout the codebase
- **Async Support** with FastAPI and SQLAlchemy

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd FanDuel
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Run the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🏃‍♂️ Quick Start

### FastAPI Development Server
```bash
uvicorn app.main:app --reload
```
Visit: http://localhost:8000

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
isort .
```

## 📁 Project Structure

```
FanDuel/
├── app/                     # Main application package
│   ├── __init__.py
│   ├── main.py             # FastAPI application entry point
│   ├── config.py           # Configuration settings
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── api/                # API routes
│   │   └── v1/            # API version 1
│   ├── core/              # Core functionality
│   │   └── database.py    # Database configuration
│   └── services/          # Business logic layer
├── alembic/               # Database migrations
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
├── .gitignore           # Git ignore file
├── README.md            # This file
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Multi-service setup
└── nginx.conf           # Reverse proxy configuration
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file based on `env.example`:

```env
# Application
APP_NAME=FanDuel Platform API
DEBUG=True
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/fanduel_db

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 🧪 Testing

The project includes comprehensive testing setup:

- **Unit Tests**: Using pytest and pytest-asyncio
- **Integration Tests**: API endpoint testing with httpx
- **Coverage**: Test coverage reporting

Run tests with:
```bash
pytest --cov=app --cov-report=html
```

## 📚 API Documentation

- **Swagger UI**: Interactive API documentation at `/docs`
- **ReDoc**: Alternative documentation at `/redoc`
- **OpenAPI Schema**: Machine-readable schema at `/openapi.json`

## 🐳 Docker Support

Build and run with Docker:

```bash
docker-compose up --build
```

## 🚀 Deployment Ready

This template includes:

- **Production Settings**: Optimized for production deployment
- **Health Checks**: Built-in health check endpoints
- **Security Headers**: CORS and security middleware
- **Logging**: Structured logging with structlog
- **Monitoring**: Ready for integration

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run code quality checks
6. Submit a pull request

## 📄 License

This template is provided for the FanDuel tech test and learning purposes.
