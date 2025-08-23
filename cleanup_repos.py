#!/usr/bin/env python3
"""
Script to clean up test repositories.
"""
import httpx
import asyncio
from app.config import settings

async def list_repositories():
    """List all repositories in the organization."""
    headers = {
        "Authorization": f"token {settings.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/orgs/{settings.github_organization}/repos",
            headers=headers
        )
        
        if response.status_code == 200:
            repos = response.json()
            print(f"📋 Found {len(repos)} repositories:")
            print("-" * 60)
            
            for i, repo in enumerate(repos, 1):
                print(f"{i:2d}. {repo['name']:<30} | Created: {repo['created_at'][:10]} | Private: {repo['private']}")
            
            return repos
        else:
            print(f"❌ Error: {response.status_code}")
            return []

async def delete_repository(repo_name):
    """Delete a specific repository."""
    headers = {
        "Authorization": f"token {settings.github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"https://api.github.com/repos/{settings.github_organization}/{repo_name}",
            headers=headers
        )
        
        if response.status_code == 204:
            print(f"✅ Deleted {repo_name}")
            return True
        else:
            print(f"❌ Failed to delete {repo_name}: {response.status_code}")
            return False

async def cleanup_test_repos():
    """Clean up test repositories."""
    repos = await list_repositories()
    
    if not repos:
        return
    
    # Filter test repositories but preserve important ones
    test_repos = [repo for repo in repos if repo['name'].startswith('platform-test-')]
    
    # Define repositories to preserve
    preserve_repos = [
        'platform-engineering-api',  # Main platform API
        'platform-test-v15',         # Latest successful test
    ]
    
    # Filter out repositories to preserve
    repos_to_delete = []
    repos_to_preserve = []
    
    for repo in test_repos:
        if repo['name'] in preserve_repos:
            repos_to_preserve.append(repo['name'])
        else:
            repos_to_delete.append(repo['name'])
    
    if not repos_to_delete:
        print("No test repositories to delete.")
        return
    
    print(f"\n🛡️  Preserving these repositories:")
    for repo in repos_to_preserve:
        print(f"  ✅ {repo}")
    
    print(f"\n🧹 Found {len(repos_to_delete)} test repositories to clean up:")
    for repo in repos_to_delete:
        print(f"  🗑️  {repo}")
    
    # Ask for confirmation
    response = input(f"\n❓ Delete all {len(repos_to_delete)} test repositories? (y/N): ")
    
    if response.lower() == 'y':
        print("\n🗑️ Deleting repositories...")
        deleted_count = 0
        
        for repo in repos_to_delete:
            if await delete_repository(repo):
                deleted_count += 1
        
        print(f"\n✅ Successfully deleted {deleted_count}/{len(repos_to_delete)} repositories.")
    else:
        print("❌ Cleanup cancelled.")

if __name__ == "__main__":
    asyncio.run(cleanup_test_repos())
