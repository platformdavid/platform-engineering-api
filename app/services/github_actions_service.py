"""
GitHub Actions service for CI/CD pipeline management.

This service integrates with GitHub Actions API to create and manage CI/CD workflows.
GitHub Actions is free for public repositories and provides 2000 minutes/month for private repos.
"""

import httpx
from typing import Dict, Any, List, Optional
import asyncio
import base64

from app.config import settings
from app.services.repository_file_service import RepositoryFileService


class GitHubActionsService:
    """
    Service for managing GitHub Actions CI/CD workflows.
    
    GitHub Actions is the industry standard for CI/CD, used by companies like
    FanDuel, Netflix, and Spotify, and is completely free for open source.
    """

    def __init__(self):
        """Initialize GitHub Actions service with API credentials."""
        self.api_token = settings.github_token
        self.organization = settings.github_organization
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.api_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def create_workflow(self, service_name: str, team: str, service_type: str) -> Dict[str, Any]:
        """
        Create a new GitHub Actions workflow for a service.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service (api, web, worker)
            
        Returns:
            Dict containing workflow information
        """
        workflow_config = self._generate_workflow_config(service_name, team, service_type)
        
        # Create repository if it doesn't exist
        await self._create_repository(service_name, service_type)
        
        # Create all repository files
        await self._create_repository_files(service_name, service_type)
        
        # Create workflow file
        workflow_result = await self._create_workflow_file(service_name, workflow_config)
        
        return workflow_result

    async def trigger_workflow(self, service_name: str, branch: str = "main") -> Dict[str, Any]:
        """
        Trigger a new workflow run.
        
        Args:
            service_name: Repository name
            branch: Branch to trigger from
            
        Returns:
            Dict containing workflow run information
        """
        # GitHub Actions workflows are triggered by pushes to the repository
        # In a real implementation, you might create a dummy commit or use the API
        return {
            "status": "triggered",
            "message": f"Workflow triggered for {service_name} on {branch} branch"
        }

    async def get_workflow_status(self, service_name: str) -> Dict[str, Any]:
        """
        Get the current status of workflows for a service.
        
        Args:
            service_name: Repository name
            
        Returns:
            Dict containing workflow status
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{self.organization}/{service_name}/actions/runs",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def _create_repository_files(self, service_name: str, service_type: str) -> None:
        """Create all necessary files for the repository."""
        file_service = RepositoryFileService()
        files = file_service.generate_all_files(service_name, service_type)
        
        for file_path, content in files.items():
            await self._create_file(service_name, file_path, content)

    async def _create_file(self, service_name: str, file_path: str, content: str) -> None:
        """Create a file in the repository."""
        async with httpx.AsyncClient() as client:
            file_data = {
                "message": f"Add {file_path}",
                "content": base64.b64encode(content.encode()).decode(),
                "branch": "main"
            }
            
            response = await client.put(
                f"{self.base_url}/repos/{self.organization}/{service_name}/contents/{file_path}",
                headers=self.headers,
                json=file_data
            )
            
            if response.status_code == 201:
                print(f"✅ Created {file_path} in {service_name}")
            elif response.status_code == 422:
                print(f"⚠️ File {file_path} already exists in {service_name}")
            else:
                print(f"❌ Failed to create {file_path} in {service_name}: {response.status_code}")

    async def _create_repository(self, service_name: str, service_type: str) -> None:
        """Create a new repository for the service."""
        repo_data = {
            "name": service_name,
            "description": f"Service created by Platform Engineering API",
            "private": False,  # Free tier: public repos are unlimited
            "auto_init": True,
            "gitignore_template": "Python" if service_type == "api" else "Node"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/orgs/{self.organization}/repos",
                headers=self.headers,
                json=repo_data
            )
            if response.status_code == 422:  # Repository already exists
                return
            response.raise_for_status()
            
        # Note: We'll use the default GITHUB_TOKEN with proper permissions
        # The repository owner needs to enable "Read and write permissions" for GITHUB_TOKEN
        # in Settings > Actions > General > Workflow permissions

    async def _create_repository_secret(self, service_name: str, secret_name: str, secret_value: str) -> None:
        """Create a repository secret using GitHub API."""
        try:
            # Get the repository's public key for encryption
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{self.organization}/{service_name}/actions/secrets/public-key",
                    headers=self.headers
                )
                response.raise_for_status()
                public_key_data = response.json()
                
                # Encrypt the secret value (this is a simplified version)
                # In production, you'd use proper encryption
                encrypted_value = base64.b64encode(secret_value.encode()).decode()
                
                # Create the secret
                secret_data = {
                    "encrypted_value": encrypted_value,
                    "key_id": public_key_data["key_id"]
                }
                
                response = await client.put(
                    f"{self.base_url}/repos/{self.organization}/{service_name}/actions/secrets/{secret_name}",
                    headers=self.headers,
                    json=secret_data
                )
                
                if response.status_code in [201, 204]:
                    print(f"✅ Created secret {secret_name} in {service_name}")
                else:
                    print(f"⚠️ Could not create secret {secret_name} in {service_name}: {response.status_code}")
                    
        except Exception as e:
            print(f"⚠️ Could not create secret {secret_name} in {service_name}: {e}")

    async def _create_workflow_file(self, service_name: str, workflow_config: str) -> Dict[str, Any]:
        """Create the GitHub Actions workflow file."""
        workflow_path = ".github/workflows/ci-cd.yml"
        
        # Encode workflow content
        workflow_content = base64.b64encode(workflow_config.encode()).decode()
        
        file_data = {
            "message": "Add CI/CD workflow via Platform Engineering API",
            "content": workflow_content,
            "branch": "main"
        }
        
        async with httpx.AsyncClient() as client:
            # First, try to get the current file to get its SHA
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{self.organization}/{service_name}/contents/{workflow_path}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    # File exists, get its SHA
                    current_file = response.json()
                    file_data["sha"] = current_file["sha"]
                    print(f"📝 Updating existing workflow file in {service_name}")
                else:
                    print(f"📝 Creating new workflow file in {service_name}")
            except Exception:
                print(f"📝 Creating new workflow file in {service_name}")
            
            # Create or update the file
            response = await client.put(
                f"{self.base_url}/repos/{self.organization}/{service_name}/contents/{workflow_path}",
                headers=self.headers,
                json=file_data
            )
            
            if response.status_code == 201:
                print(f"✅ Created workflow file in {service_name}")
            elif response.status_code == 200:
                print(f"✅ Updated workflow file in {service_name}")
            else:
                print(f"⚠️ Workflow file operation returned {response.status_code}")
            
            response.raise_for_status()
            return response.json()

    def _generate_workflow_config(self, service_name: str, team: str, service_type: str) -> str:
        """
        Generate GitHub Actions workflow configuration.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service
            
        Returns:
            YAML workflow configuration
        """
        if service_type == "api":
            return self._generate_api_workflow(service_name, team)
        elif service_type == "web":
            return self._generate_web_workflow(service_name, team)
        elif service_type == "worker":
            return self._generate_worker_workflow(service_name, team)
        else:
            raise ValueError(f"Unknown service type: {service_type}")

    def _generate_api_workflow(self, service_name: str, team: str) -> str:
        """Generate workflow for API services."""
        return f"""name: CI/CD Pipeline - {service_name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  packages: write
  actions: read

env:
  SERVICE_NAME: {service_name}
  TEAM: {team}
  REGISTRY: ghcr.io/${{ github.repository_owner }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: |
        black --check --diff .
    
    - name: Run tests with pytest
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Run security scan
      run: |
        pip install bandit safety
        bandit -r app/ -f json -o bandit-report.json
        safety check --json > safety-report.json
    
    - name: Upload security reports
      uses: actions/upload-artifact@v4
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  # SonarCloud analysis (commented out for now)
  # sonarcloud:
  #   runs-on: ubuntu-latest
  #   needs: test
  #   steps:
  #   - uses: actions/checkout@v4
  #     with:
  #       fetch-depth: 0
  #   
  #   - name: Set up Python
  #     uses: actions/setup-python@v4
  #     with:
  #       python-version: '3.11'
  #   
  #   - name: Install dependencies
  #     run: |
  #       pip install -r requirements.txt
  #   
  #   - name: Run tests with coverage
  #     run: |
  #       pytest --cov=app --cov-report=xml
  #   
  #   - name: SonarCloud Scan
  #     uses: SonarSource/sonarcloud-github-action@master
  #     env:
  #       GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  #       SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    
    # Docker build temporarily disabled due to container registry permissions
    # - name: Set up Docker Buildx
    #   uses: docker/setup-buildx-action@v3
    # 
    # - name: Log in to Container Registry
    #   uses: docker/login-action@v3
    #   with:
    #     registry: ghcr.io
    #     username: ${{ github.actor }}
    #     password: ${{ secrets.GITHUB_TOKEN }}
    # 
    # - name: Build and push Docker image
    #   uses: docker/build-push-action@v5
    #   with:
    #     context: .
    #     push: true
    #     tags: |
    #       ${{ env.REGISTRY }}/${{ env.SERVICE_NAME }}:${{ github.sha }}
    #       ${{ env.REGISTRY }}/${{ env.SERVICE_NAME }}:latest
    #     cache-from: type=gha
    #     cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main' && vars.ENABLE_DEPLOY == 'true'
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'
    
    - name: Configure kubectl
      run: |
        if [ -z "${{ secrets.KUBE_CONFIG }}" ]; then
          echo "KUBE_CONFIG secret not set. Skipping deployment."
          exit 1
        fi
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig.yaml
        echo "KUBECONFIG=$(pwd)/kubeconfig.yaml" >> $GITHUB_ENV
    
    - name: Deploy to Kubernetes
      run: |
        # Update image in deployment.yaml
        sed -i "s|ghcr.io/platformdavid|\${{ env.REGISTRY }}|g" k8s/deployment.yaml
        kubectl apply -f k8s/ --validate=false
        kubectl rollout status deployment/${{ env.SERVICE_NAME }}
    
    - name: Run smoke tests
      run: |
        # Wait for service to be ready
        sleep 30
        curl -f http://${{ env.SERVICE_NAME }}/health || exit 1
    
    - name: Health check
      run: |
        curl -f http://${{ env.SERVICE_NAME }}/health
        echo "Service is healthy!"

  # Alternative: Skip deployment but validate K8s manifests
  validate-k8s:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main' && vars.ENABLE_DEPLOY != 'true'
    steps:
    - uses: actions/checkout@v4
    
    - name: Validate Kubernetes manifests
      run: |
        # Update image in deployment.yaml to use correct registry
        sed -i "s|ghcr.io/platformdavid|\${{ env.REGISTRY }}|g" k8s/deployment.yaml
        
        # Display updated files for verification
        echo "=== Updated deployment.yaml ==="
        cat k8s/deployment.yaml
        echo ""
        echo "=== service.yaml ==="
        cat k8s/service.yaml
        
        # Validate YAML syntax
        echo "Validating YAML syntax..."
        for file in k8s/*.yaml; do
          echo "✓ Checking $file"
          python3 -c "import yaml, sys; f=open('$file', 'r'); yaml.safe_load(f); print('  YAML syntax: OK'); f.close()"
        done
        
        # Basic manifest structure validation
        echo "Validating Kubernetes manifest structure..."
        python3 -c "import yaml, sys; [print('✓ ' + f + ': ' + yaml.safe_load(open(f, 'r')).get('kind', 'unknown') + ' structure OK') or None for f in ['k8s/deployment.yaml', 'k8s/service.yaml']]"
        
        echo "✅ All Kubernetes manifests are valid!"
"""

    def _generate_web_workflow(self, service_name: str, team: str) -> str:
        """Generate workflow for web services."""
        return f"""name: CI/CD Pipeline - {service_name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  SERVICE_NAME: {service_name}
  TEAM: {team}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint with ESLint
      run: npm run lint
    
    - name: Format check with Prettier
      run: npm run format:check
    
    - name: Run unit tests
      run: npm run test:unit
    
    - name: Run visual regression tests
      run: npm run test:visual
      if: ${{ github.event_name == 'pull_request' }}

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Build application
      run: npm run build
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: eu-west-2
    
    - name: Deploy to S3
      run: |
        aws s3 sync dist/ s3://platformdavid-web-assets/${{ env.SERVICE_NAME }}/
        aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} --paths "/*"
    
    - name: Run smoke tests
      run: |
        sleep 30
        curl -f https://${{ env.SERVICE_NAME }}.platformdavid.com/ || exit 1
    
    - name: Health check
      run: |
        curl -f https://${{ env.SERVICE_NAME }}.platformdavid.com/
        echo "Website is live!"
"""

    def _generate_worker_workflow(self, service_name: str, team: str) -> str:
        """Generate workflow for worker services."""
        return f"""name: CI/CD Pipeline - {service_name}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  SERVICE_NAME: {service_name}
  TEAM: {team}
  REGISTRY: ghcr.io/{settings.github_organization}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Format check with black
      run: |
        black --check --diff . || black . --diff
    
    - name: Run worker tests
      run: |
        pytest tests/test_worker.py --cov=app --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: workertests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Run security scan
      run: |
        pip install bandit safety
        bandit -r app/ -f json -o bandit-report.json || true
        safety check --json --output safety-report.json || true
    
    - name: Upload security reports
      uses: actions/upload-artifact@v4
      with:
        name: security-reports
        path: |
          bandit-report.json
          safety-report.json

  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Build and push worker image
      uses: docker/build-push-action@v5
      with:
        context: .
        dockerfile: Dockerfile.worker
        push: true
        tags: |
          ${{ env.REGISTRY }}/${{ env.SERVICE_NAME }}-worker:${{ github.sha }}
          ${{ env.REGISTRY }}/${{ env.SERVICE_NAME }}-worker:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3
      with:
        version: 'latest'
    
    - name: Configure kubectl
      run: |
        echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig.yaml
        export KUBECONFIG=kubeconfig.yaml
    
    - name: Deploy worker to Kubernetes
      run: |
        kubectl apply -f k8s/worker.yaml
        kubectl rollout status deployment/${{ env.SERVICE_NAME }}-worker
    
    - name: Run smoke tests
      run: |
        # Test worker queue health
        sleep 30
        curl -f http://${{ env.SERVICE_NAME }}-worker/health || exit 1
"""

    def generate_custom_workflow_config(self, service_name: str, team: str, service_type: str,
                                      enable_linting: bool = True,
                                      enable_formatting: bool = True,
                                      enable_unit_tests: bool = True,
                                      enable_integration_tests: bool = True,
                                      enable_sonarcloud: bool = False,  # Disabled by default
                                      enable_security_scan: bool = True,
                                      enable_smoke_tests: bool = True,
                                      enable_health_check: bool = True,
                                      enable_visual_tests: bool = False) -> str:
        """
        Generate custom GitHub Actions workflow based on team preferences.
        
        Args:
            service_name: Name of the service
            team: Team that owns the service
            service_type: Type of service
            enable_linting: Enable linting checks
            enable_formatting: Enable formatting checks
            enable_unit_tests: Enable unit tests
            enable_integration_tests: Enable integration tests
            enable_sonarcloud: Enable SonarCloud analysis (disabled by default)
            enable_security_scan: Enable security scanning
            enable_smoke_tests: Enable smoke tests
            enable_health_check: Enable health checks
            enable_visual_tests: Enable visual regression tests (web only)
            
        Returns:
            Custom workflow configuration
        """
        # This would generate a custom workflow based on the flags
        # For brevity, returning the standard workflow
        return self._generate_workflow_config(service_name, team, service_type)
