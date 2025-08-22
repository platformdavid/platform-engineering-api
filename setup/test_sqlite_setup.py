#!/usr/bin/env python3
"""
Test SQLite database setup script.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Set environment variable for SQLite
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./platform_engineering.db"

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.service import Service, ServiceType, Environment, ServiceStatus


async def test_database_connection():
    """Test database connection and create a simple table."""
    print("🧪 Testing SQLite database connection...")
    
    try:
        # Initialize database
        await init_db()
        print("✅ Database tables created successfully!")
        
        # Test creating a simple service
        async with AsyncSessionLocal() as db:
            test_service = Service(
                name="test-service",
                team="test-team",
                service_type=ServiceType.API,
                environment=Environment.STAGING,
                description="Test service for database verification",
                tags=["test", "api"],
                configuration={"framework": "fastapi"},
                infrastructure_config={"cpu": "100m", "memory": "128Mi"},
                monitoring_config={"metrics": ["requests"]},
                status=ServiceStatus.PENDING
            )
            
            db.add(test_service)
            await db.commit()
            print("✅ Test service created successfully!")
            
            # Query the service back
            result = await db.get(Service, test_service.id)
            if result:
                print(f"✅ Service retrieved: {result.name}")
            else:
                print("❌ Failed to retrieve service")
                
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        raise


async def main():
    """Main test function."""
    print("🚀 Testing Platform Engineering Database with SQLite...")
    
    try:
        await test_database_connection()
        print("\n🎉 SQLite database test completed successfully!")
        print("\n📋 What was tested:")
        print("  - Database connection")
        print("  - Table creation")
        print("  - Data insertion")
        print("  - Data retrieval")
        
        print("\n🔗 Next steps:")
        print("  1. SQLite database is working!")
        print("  2. You can now run the full setup: python setup/setup_database.py")
        
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
