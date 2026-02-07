#!/usr/bin/env python3
"""
Script to push the Banking Bot code to GitHub
"""
import os
from git import Repo
from git.exc import InvalidGitRepositoryError
import git

# Set the git executable path
git.refresh('C:\\Program Files\\Git\\bin\\git.exe')

def push_to_github():
    """Initialize git repository and push to GitHub"""
    repo_path = r"c:\banking bot"
    github_url = "https://github.com/shedaahmad/Bank.git"
    email = "shedaahmad@gmail.com"
    username = "shedaahmad"
    
    os.chdir(repo_path)
    
    try:
        # Check if repository already exists
        repo = Repo(repo_path)
        print("✓ Repository already initialized")
    except InvalidGitRepositoryError:
        # Initialize new repository
        print("📦 Initializing new repository...")
        repo = Repo.init(repo_path)
        print("✓ Repository initialized")
    
    # Configure git
    with repo.config_writer() as git_config:
        git_config.set_value("user", "email", email)
        git_config.set_value("user", "name", username)
    print(f"✓ Git configured for {username} ({email})")
    
    # Add all files
    print("📄 Adding files...")
    repo.index.add([item[0] for item in repo.index.entries.keys()])
    repo.index.add('*')
    print("✓ Files added")
    
    # Commit
    try:
        commit = repo.index.commit("Initial commit: Banking Bot with Mistral AI integration")
        print(f"✓ Committed: {commit.hexsha[:7]}")
    except Exception as e:
        print(f"⚠ Commit warning: {e}")
    
    # Add remote
    try:
        origin = repo.remote('origin')
        origin.set_url(github_url)
        print(f"✓ Remote 'origin' updated: {github_url}")
    except ValueError:
        origin = repo.create_remote('origin', github_url)
        print(f"✓ Remote 'origin' created: {github_url}")
    
    # Push to GitHub
    print("🚀 Pushing to GitHub...")
    try:
        origin.push(refspec='HEAD:main')
        print("✓ Successfully pushed to GitHub (main branch)")
    except Exception as e:
        try:
            # Try pushing to master if main doesn't exist
            origin.push(refspec='HEAD:master')
            print("✓ Successfully pushed to GitHub (master branch)")
        except Exception as e2:
            print(f"❌ Push failed: {e2}")
            print("\nNote: You may need to:")
            print("1. Set up GitHub authentication (PAT or SSH key)")
            print("2. Ensure the repository exists on GitHub")
            return False
    
    print("\n✅ All done! Your Banking Bot code has been pushed to GitHub.")
    print(f"Repository: {github_url}")
    return True

if __name__ == "__main__":
    push_to_github()
