#!/usr/bin/env python3
"""
Setup script to help users configure GitHub Pages deployment.
"""

import os
import json
import subprocess

def check_git_repository():
    """Check if we're in a git repository."""
    try:
        result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                              capture_output=True, text=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_repository_info():
    """Get GitHub repository information."""
    try:
        # Get remote URL
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True, check=True)
        remote_url = result.stdout.strip()
        
        # Extract owner and repo name
        if 'github.com' in remote_url:
            if remote_url.startswith('https://'):
                # https://github.com/owner/repo.git
                parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
            else:
                # git@github.com:owner/repo.git
                parts = remote_url.replace('git@github.com:', '').replace('.git', '').split('/')
            
            if len(parts) >= 2:
                return parts[0], parts[1]
    except subprocess.CalledProcessError:
        pass
    
    return None, None

def create_github_pages_config():
    """Create GitHub Pages configuration files."""
    print("📄 Creating GitHub Pages configuration...")
    
    # Create docs directory
    os.makedirs('docs', exist_ok=True)
    
    # Create Jekyll config
    jekyll_config = """
# GitHub Pages Jekyll Configuration
title: Stock Moon Dashboard
description: Analyzing relationships between stock prices and moon phases
baseurl: ""
url: ""

# Build settings
markdown: kramdown
highlighter: rouge
theme: minima

# Exclude files
exclude:
  - README.md
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
  - .sass-cache
  - .jekyll-cache
  - .jekyll-metadata

# Include files
include:
  - _pages

# Collections
collections:
  pages:
    output: true
    permalink: /:name/

# Defaults
defaults:
  - scope:
      path: ""
      type: "pages"
    values:
      layout: "default"
"""
    
    with open('docs/_config.yml', 'w') as f:
        f.write(jekyll_config.strip())
    
    # Create index redirect
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Moon Dashboard</title>
    <meta http-equiv="refresh" content="0; url=./demo/">
    <link rel="canonical" href="./demo/">
</head>
<body>
    <p>Redirecting to <a href="./demo/">Stock Moon Dashboard Demo</a>...</p>
</body>
</html>
"""
    
    with open('docs/index.html', 'w') as f:
        f.write(index_html.strip())
    
    print("✅ GitHub Pages configuration created")

def update_workflow_files():
    """Update workflow files with repository information."""
    owner, repo = get_repository_info()
    
    if owner and repo:
        print(f"📝 Updating workflows for {owner}/{repo}...")
        
        # Update generate_static_demo.py
        try:
            with open('generate_static_demo.py', 'r') as f:
                content = f.read()
            
            content = content.replace('yourusername', owner)
            content = content.replace('stock-moon-dashboard', repo)
            
            with open('generate_static_demo.py', 'w') as f:
                f.write(content)
            
            print("✅ Updated generate_static_demo.py")
        except Exception as e:
            print(f"⚠️  Could not update generate_static_demo.py: {e}")
    else:
        print("⚠️  Could not detect repository information")

def main():
    """Main setup function."""
    print("🚀 Setting up GitHub Pages for Stock Moon Dashboard")
    print("=" * 60)
    
    # Check if we're in a git repository
    if not check_git_repository():
        print("❌ This doesn't appear to be a git repository.")
        print("💡 Initialize git first: git init")
        return False
    
    # Get repository info
    owner, repo = get_repository_info()
    if owner and repo:
        print(f"📂 Repository: {owner}/{repo}")
        pages_url = f"https://{owner}.github.io/{repo}/"
        print(f"🌐 Future Pages URL: {pages_url}")
    else:
        print("⚠️  Could not detect GitHub repository information")
        print("💡 Make sure you have a GitHub remote configured")
    
    print()
    
    # Create configuration files
    create_github_pages_config()
    update_workflow_files()
    
    print()
    print("📋 Next Steps:")
    print("1. Commit and push all files:")
    print("   git add .")
    print("   git commit -m 'Setup GitHub Pages deployment'")
    print("   git push origin main")
    print()
    print("2. Enable GitHub Pages in repository settings:")
    print("   • Go to repository Settings → Pages")
    print("   • Source: Deploy from a branch")
    print("   • Branch: main / docs")
    print("   • Or use GitHub Actions (recommended)")
    print()
    print("3. Wait for deployment (usually 1-2 minutes)")
    
    if owner and repo:
        print(f"4. Visit your demo: https://{owner}.github.io/{repo}/")
    
    print()
    print("🎉 GitHub Pages setup complete!")
    print("💡 The workflow will automatically generate and deploy your demo")
    
    return True

if __name__ == "__main__":
    main()