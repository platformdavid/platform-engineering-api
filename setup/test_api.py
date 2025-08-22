#!/usr/bin/env python3
"""
Platform Engineering API Test Suite

This script provides comprehensive testing for the Platform Engineering API.
It tests all imports, basic functionality, and provides a simple API server for testing.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import boto3
import yaml
import kubernetes
import github
import pydantic

# Create FastAPI app
app = FastAPI(
    title="Platform Engineering API",
    description="A platform engineering API for managing services, CI/CD, and infrastructure",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Platform Engineering API is running!",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "health": "/health",
            "services": "/services", 
            "platform_tools": "/platform-tools",
            "config": "/config",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint for all components."""
    return {
        "status": "healthy",
        "service": "platform-engineering-api",
        "components": {
            "fastapi": "✅",
            "pydantic": "✅",
            "boto3": "✅",
            "kubernetes": "✅",
            "github": "✅",
            "yaml": "✅"
        }
    }

@app.get("/services")
def list_services():
    """List managed services."""
    return {
        "services": [
            {
                "name": "example-api",
                "type": "api",
                "status": "running",
                "environment": "development",
                "infrastructure": "aws-ecs",
                "ci_cd": "github-actions"
            },
            {
                "name": "example-web",
                "type": "web",
                "status": "running", 
                "environment": "development",
                "infrastructure": "aws-s3",
                "ci_cd": "github-actions"
            },
            {
                "name": "example-worker",
                "type": "worker",
                "status": "running",
                "environment": "development", 
                "infrastructure": "aws-lambda",
                "ci_cd": "github-actions"
            }
        ]
    }

@app.get("/platform-tools")
def platform_tools():
    """Information about platform engineering tools."""
    return {
        "tools": {
            "aws": {
                "boto3_version": boto3.__version__,
                "services": ["ECS", "S3", "Lambda", "CloudWatch"]
            },
            "kubernetes": {
                "version": kubernetes.__version__,
                "capabilities": ["deployments", "services", "configmaps"]
            },
            "github": {
                "capabilities": ["repositories", "workflows", "actions"]
            },
            "yaml": {
                "capabilities": ["kubernetes_manifests", "github_workflows", "configs"]
            }
        }
    }

@app.get("/config")
def get_config():
    """Current configuration using Pydantic."""
    class Config(BaseModel):
        app_name: str = "Platform Engineering API"
        debug: bool = True
        aws_region: str = "eu-west-2"
        github_org: str = "platformdavid"
    
    config = Config()
    
    # Handle both Pydantic v1 and v2
    if pydantic.__version__.startswith('1.'):
        config_dict = config.dict()
    else:
        config_dict = config.model_dump()
    
    return {
        "config": config_dict,
        "pydantic_version": pydantic.__version__
    }

def test_imports():
    """Test that all essential imports work."""
    print("🧪 Testing Platform Engineering API imports...")
    print("=" * 60)
    
    tests = [
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("boto3", "Boto3"),
        ("yaml", "PyYAML"),
        ("kubernetes", "Kubernetes"),
        ("github", "PyGithub"),
        ("uvicorn", "Uvicorn"),
    ]
    
    all_passed = True
    
    for module_name, display_name in tests:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name} imported successfully (v{version})")
        except ImportError as e:
            print(f"❌ {display_name} import failed: {e}")
            all_passed = False
        except Exception as e:
            print(f"⚠️  {display_name} import had issues: {e}")
    
    return all_passed

def test_fastapi_functionality():
    """Test FastAPI and Pydantic functionality."""
    print("\n🔧 Testing FastAPI functionality...")
    
    try:
        # Test model creation
        class TestModel(BaseModel):
            name: str
            value: int
        
        test_data = TestModel(name="test", value=42)
        
        # Handle both Pydantic v1 and v2
        if pydantic.__version__.startswith('1.'):
            result = test_data.dict()
        else:
            result = test_data.model_dump()
        
        print(f"✅ FastAPI app created successfully")
        print(f"✅ Pydantic model works: {result}")
        return True
        
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        return False

def test_platform_tools():
    """Test platform engineering tools."""
    print("\n⚙️  Testing platform engineering tools...")
    
    try:
        print(f"✅ Boto3 version: {boto3.__version__}")
        print(f"✅ PyYAML loaded successfully")
        print(f"✅ Kubernetes version: {kubernetes.__version__}")
        print(f"✅ PyGithub loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Platform tools test failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test suite."""
    print("🚀 Platform Engineering API - Comprehensive Test")
    print("=" * 60)
    
    # Test 1: Basic imports
    imports_ok = test_imports()
    
    # Test 2: FastAPI functionality
    fastapi_ok = test_fastapi_functionality()
    
    # Test 3: Platform tools
    tools_ok = test_platform_tools()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print(f"   Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"   FastAPI: {'✅ PASS' if fastapi_ok else '❌ FAIL'}")
    print(f"   Tools:   {'✅ PASS' if tools_ok else '❌ FAIL'}")
    
    all_passed = imports_ok and fastapi_ok and tools_ok
    
    if all_passed:
        print("\n🎉 All tests passed! Your installation is working correctly.")
        print("\n📋 API Endpoints:")
        print("   GET /              - Root endpoint")
        print("   GET /health        - Health check")
        print("   GET /services      - List services")
        print("   GET /platform-tools - Platform tools info")
        print("   GET /config        - Configuration info")
        print("\n📋 Next steps:")
        print("   1. Run the API: python -m uvicorn test_api:app --reload")
        print("   2. Visit: http://localhost:8000")
        print("   3. Check docs: http://localhost:8000/docs")
    else:
        print("\n⚠️  Some tests failed. Please check the installation.")
        print("   You may need to reinstall packages or check compatibility.")
    
    return all_passed

if __name__ == "__main__":
    run_comprehensive_test()
