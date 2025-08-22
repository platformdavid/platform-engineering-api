#!/usr/bin/env python3
"""
Platform Engineering API Installation Script

This script installs all required packages for the Platform Engineering API.
It handles compatibility issues and provides comprehensive error reporting.
"""

import subprocess
import sys
import os
from typing import List, Dict, Tuple

def run_command(command: List[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def install_package(package: str, description: str = None) -> bool:
    """Install a single package."""
    if description is None:
        description = f"Installing {package}"
    
    return run_command([sys.executable, "-m", "pip", "install", package], description)

def install_packages(packages: List[str], description: str) -> bool:
    """Install multiple packages."""
    return run_command([sys.executable, "-m", "pip", "install"] + packages, description)

def install_with_binary_flag(packages: List[str], description: str) -> bool:
    """Install packages with --only-binary=all flag."""
    return run_command([sys.executable, "-m", "pip", "install", "--only-binary=all"] + packages, description)

def verify_installation() -> Tuple[bool, Dict[str, str]]:
    """Verify that all packages are installed correctly."""
    print("\n✅ Verifying installation...")
    
    verification_packages = [
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("boto3", "Boto3"),
        ("yaml", "PyYAML"),
        ("kubernetes", "Kubernetes"),
        ("github", "PyGithub"),
        ("uvicorn", "Uvicorn"),
        ("pydantic_settings", "Pydantic Settings"),
        ("structlog", "Structlog"),
    ]
    
    results = {}
    all_good = True
    
    for module_name, display_name in verification_packages:
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {display_name} imported successfully (v{version})")
            results[module_name] = version
        except ImportError as e:
            print(f"❌ {display_name} import failed: {e}")
            results[module_name] = "FAILED"
            all_good = False
        except Exception as e:
            print(f"⚠️  {display_name} import had issues: {e}")
            results[module_name] = "ISSUES"
    
    return all_good, results

def main():
    """Main installation process."""
    print("🚀 Platform Engineering API - Installation")
    print("=" * 60)
    print("This script will install all required packages for the Platform Engineering API.")
    print("=" * 60)
    
    # Step 1: Upgrade pip
    print("\n📦 Step 1: Upgrading pip...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")
    
    # Step 2: Clean up any existing incompatible installations
    print("\n🧹 Step 2: Cleaning up existing installations...")
    cleanup_packages = ["pydantic", "pydantic-core", "pydantic-settings", "fastapi", "uvicorn"]
    run_command([sys.executable, "-m", "pip", "uninstall"] + cleanup_packages + ["-y"], 
                "Removing existing packages")
    
    # Step 3: Install core FastAPI packages with binary flag
    print("\n🔧 Step 3: Installing core FastAPI packages...")
    core_packages = ["fastapi", "uvicorn[standard]", "pydantic"]
    
    if not install_with_binary_flag(core_packages, "Installing core FastAPI packages"):
        print("❌ Core packages installation failed. Stopping.")
        return False
    
    # Step 4: Install additional packages
    print("\n📝 Step 4: Installing additional packages...")
    additional_packages = [
        "pydantic-settings",
        "structlog==23.2.0"
    ]
    
    install_packages(additional_packages, "Installing additional packages")
    
    # Step 5: Install testing packages
    print("\n🧪 Step 5: Installing testing packages...")
    testing_packages = [
        "pytest==7.4.3",
        "pytest-asyncio==0.21.1",
        "httpx==0.25.2"
    ]
    
    install_packages(testing_packages, "Installing testing packages")
    
    # Step 6: Install code quality packages
    print("\n🎨 Step 6: Installing code quality packages...")
    quality_packages = [
        "black==23.12.1",
        "flake8==6.1.0",
        "isort==5.12.0",
        "mypy==1.7.1"
    ]
    
    install_packages(quality_packages, "Installing code quality packages")
    
    # Step 7: Install utility packages
    print("\n🔧 Step 7: Installing utility packages...")
    utility_packages = [
        "python-dotenv==1.0.0"
    ]
    
    install_packages(utility_packages, "Installing utility packages")
    
    # Step 8: Install platform engineering tools
    print("\n⚙️  Step 8: Installing platform engineering tools...")
    platform_packages = [
        "pyyaml==6.0.1",
        "boto3==1.34.0",
        "botocore==1.34.0",
        "kubernetes==28.1.0",
        "PyGithub==1.59.1"
    ]
    
    install_packages(platform_packages, "Installing platform engineering tools")
    
    # Step 9: Install production server
    print("\n🚀 Step 9: Installing production server...")
    install_package("gunicorn==21.2.0", "Installing Gunicorn")
    
    # Step 10: Verify installation
    all_good, versions = verify_installation()
    
    # Final status
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 Installation completed successfully!")
        print("\n📋 Installed packages:")
        for package, version in versions.items():
            print(f"   ✅ {package}: v{version}")
        
        print("\n📋 Next steps:")
        print("1. Test the installation: python test_api.py")
        print("2. Run the API: python -m uvicorn test_api:app --reload")
        print("3. Visit: http://localhost:8000")
        print("4. Check docs: http://localhost:8000/docs")
        
    else:
        print("⚠️  Installation completed with some issues.")
        print("Some packages may need manual installation.")
        print("\n📋 Failed packages:")
        for package, version in versions.items():
            if version in ["FAILED", "ISSUES"]:
                print(f"   ❌ {package}: {version}")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
