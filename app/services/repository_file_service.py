"""
Repository file service for generating all necessary files for a service repository.

This service generates the complete file structure that will be included in the GitHub repository,
ensuring the CI/CD pipeline will work correctly.
"""

from typing import Dict, Any
from pathlib import Path


class RepositoryFileService:
    """
    Service for generating repository files.
    
    Generates all necessary files for a service repository including:
    - requirements.txt and requirements-dev.txt
    - app/ directory with main.py
    - tests/ directory with test files
    - k8s/ directory with manifests
    - Dockerfile
    - README.md
    - .gitignore
    """

    def __init__(self):
        """Initialize repository file service."""
        pass

    def generate_all_files(self, service_name: str, service_type: str = "api") -> Dict[str, str]:
        """
        Generate all files for a service repository.
        
        Args:
            service_name: Name of the service
            service_type: Type of service (api, worker, etc.)
            
        Returns:
            Dictionary mapping file paths to file contents
        """
        files = {}
        
        # Generate requirements files
        files["requirements.txt"] = self._generate_requirements_txt()
        files["requirements-dev.txt"] = self._generate_requirements_dev_txt()
        
        # Generate app files
        files["app/__init__.py"] = ""
        files["app/main.py"] = self._generate_main_py(service_name)
        
        # Generate test files
        files["tests/__init__.py"] = ""
        files["tests/test_main.py"] = self._generate_test_main_py(service_name)
        
        # Generate Kubernetes files
        files["k8s/deployment.yaml"] = self._generate_deployment_yaml(service_name)
        files["k8s/service.yaml"] = self._generate_service_yaml(service_name)
        
        # Generate Dockerfile
        files["Dockerfile"] = self._generate_dockerfile()
        
        # Generate README
        files["README.md"] = self._generate_readme(service_name)
        
        # Generate .gitignore
        files[".gitignore"] = self._generate_gitignore()
        
        return files

    def _generate_requirements_txt(self) -> str:
        """Generate requirements.txt file."""
        return """fastapi
uvicorn[standard]
pydantic
pydantic-settings"""

    def _generate_requirements_dev_txt(self) -> str:
        """Generate requirements-dev.txt file."""
        return """pytest==7.4.3
pytest-cov
pytest-asyncio==0.21.1
flake8==6.1.0
black==23.12.1
isort==5.12.0
bandit
safety
httpx==0.25.2"""

    def _generate_main_py(self, service_name: str) -> str:
        """Generate main.py file."""
        return f"""from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {{"status": "healthy"}}


@app.get("/")
def root():
    return {{"message": "Hello from {service_name}"}}
"""

    def _generate_test_main_py(self, service_name: str) -> str:
        """Generate test_main.py file."""
        return f"""from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    "Test the health check endpoint."
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {{"status": "healthy"}}


def test_root_endpoint():
    "Test the root endpoint."
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {{"message": "Hello from {service_name}"}}


def test_health_endpoint_returns_json():
    "Test that health endpoint returns proper JSON content type."
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_root_endpoint_returns_json():
    "Test that root endpoint returns proper JSON content type."
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
"""

    def _generate_deployment_yaml(self, service_name: str) -> str:
        """Generate deployment.yaml file."""
        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
    spec:
      containers:
      - name: {service_name}
        image: ghcr.io/platformdavid/{service_name}:latest
        ports:
        - containerPort: 8000
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10"""

    def _generate_service_yaml(self, service_name: str) -> str:
        """Generate service.yaml file."""
        return f"""apiVersion: v1
kind: Service
metadata:
  name: {service_name}
spec:
  selector:
    app: {service_name}
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP"""

    def _generate_dockerfile(self) -> str:
        """Generate Dockerfile."""
        return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]"""

    def _generate_readme(self, service_name: str) -> str:
        """Generate README.md file."""
        return f"""# {service_name}
Service created by Platform Engineering API."""

    def _generate_gitignore(self) -> str:
        """Generate .gitignore file."""
        return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock
#poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
#pdm.lock
#pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
#pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

# Abstra
# Abstra is an AI-powered process automation framework.
# Ignore directories containing user credentials, local state, and settings.
# Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#  Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#  that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#  and can be added to the global gitignore or merged into this file. However, if you prefer, 
#  you could uncomment the following to ignore the entire vscode folder
# .vscode/

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Cursor
#  Cursor is an AI-powered code editor. `.cursorignore` specifies files/directories to
#  exclude from AI features like autocomplete and code analysis. Recommended for sensitive data
#  refer to https://docs.cursor.com/context/ignore-files
.cursorignore
.cursorindexingignore

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/"""
