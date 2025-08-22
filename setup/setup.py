#!/usr/bin/env python3
"""
Setup script for FanDuel Platform Engineering API.

This script automates the initial setup of the FastAPI application.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a shell command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_env_file():
    """Create .env file from template."""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        try:
            with open('env.example', 'r') as template:
                content = template.read()
            
            # Generate secure keys
            import secrets
            secret_key = secrets.token_urlsafe(32)
            jwt_secret_key = secrets.token_urlsafe(32)
            
            content = content.replace('your-secret-key-here-change-in-production', secret_key)
            content = content.replace('dev-secret-key-change-in-production', secret_key)
            content = content.replace('your-jwt-secret-key-here-change-in-production', jwt_secret_key)
            content = content.replace('dev-jwt-secret-key-change-in-production', jwt_secret_key)
            
            with open('.env', 'w') as env_file:
                env_file.write(content)
            
            print("✅ .env file created successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
        return True


def main():
    """Main setup function."""
    print("🚀 Setting up FanDuel Platform Engineering API...")
    
    # Check if Python 3.11+ is available
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        sys.exit(1)
    
    # Create necessary directories
    directories = ['logs', 'app/models', 'app/schemas', 'app/api/v1/endpoints', 'tests']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Run database migrations (if using Alembic)
    print("📊 Note: Database migrations will be handled by Alembic when you run the application")
    
    # Run tests
    if not run_command("pytest --version", "Checking pytest installation"):
        print("⚠️  Pytest not available, skipping tests")
    else:
        if not run_command("pytest", "Running tests"):
            print("⚠️  Some tests failed, but setup continues")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Review and update the .env file with your configuration")
    print("2. Start the application: uvicorn app.main:app --reload")
    print("3. Visit http://localhost:8000/docs for API documentation")
    print("4. For Docker: docker-compose up --build")


if __name__ == "__main__":
    main()
