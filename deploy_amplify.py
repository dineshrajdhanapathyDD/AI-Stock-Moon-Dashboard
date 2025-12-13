#!/usr/bin/env python3
"""
AWS Amplify deployment helper script.
Prepares the project for Amplify deployment and provides setup guidance.
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def check_prerequisites():
    """Check if all prerequisites are met."""
    print("🔍 Checking prerequisites...")
    
    issues = []
    
    # Check if we're in a git repository
    try:
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, check=True)
        print("✅ Git repository detected")
    except (subprocess.CalledProcessError, FileNotFoundError):
        issues.append("❌ Not in a git repository. Run: git init")
    
    # Check if requirements.txt exists
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt found")
    else:
        issues.append("❌ requirements.txt not found")
    
    # Check if amplify.yml exists
    if os.path.exists('amplify.yml'):
        print("✅ amplify.yml configuration found")
    else:
        issues.append("❌ amplify.yml not found")
    
    # Check if app.py exists
    if os.path.exists('app.py'):
        print("✅ app.py entry point found")
    else:
        issues.append("❌ app.py not found")
    
    return issues

def validate_python_dependencies():
    """Validate that all Python dependencies are properly specified."""
    print("\n📦 Validating Python dependencies...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        # Check for essential dependencies
        essential_deps = ['dash', 'plotly', 'pandas', 'numpy', 'requests']
        missing_deps = []
        
        req_names = [req.split('==')[0].split('>=')[0].split('<=')[0] for req in requirements if req.strip()]
        
        for dep in essential_deps:
            if dep not in req_names:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"⚠️  Missing essential dependencies: {', '.join(missing_deps)}")
            return False
        else:
            print(f"✅ All essential dependencies found ({len(requirements)} total)")
            return True
            
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def create_amplify_environment_config():
    """Create environment configuration for Amplify."""
    print("\n⚙️  Creating Amplify environment configuration...")
    
    env_config = {
        "PYTHONPATH": "/opt/python:/opt/python/lib/python3.9/site-packages",
        "PORT": "8050",
        "DASH_DEBUG": "False",
        "DASH_HOST": "0.0.0.0",
        "DASH_COMPRESS": "True",
        "DASH_SERVE_LOCALLY": "False",
        "DASH_REQUESTS_PATHNAME_PREFIX": "/",
        "CACHE_TTL": "3600",
        "MAX_RETRIES": "3",
        "LOG_LEVEL": "INFO"
    }
    
    # Create environment file for reference
    with open('amplify_env_vars.json', 'w') as f:
        json.dump(env_config, f, indent=2)
    
    print("✅ Environment configuration created: amplify_env_vars.json")
    return env_config

def test_application_locally():
    """Test the application locally before deployment."""
    print("\n🧪 Testing application locally...")
    
    try:
        # Test imports
        print("Testing Python imports...")
        result = subprocess.run([
            sys.executable, '-c', 
            'from src.dashboard import app; print("Dashboard import successful")'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Application imports successfully")
        else:
            print(f"❌ Import error: {result.stderr}")
            return False
        
        # Test stock database
        result = subprocess.run([
            sys.executable, '-c',
            'from src.stock_database import stock_db; print(f"Stock database: {len(stock_db.stocks)} stocks")'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Stock database loads successfully")
        else:
            print(f"❌ Stock database error: {result.stderr}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Local testing failed: {e}")
        return False

def generate_deployment_summary():
    """Generate deployment summary and next steps."""
    print("\n📋 Deployment Summary")
    print("=" * 50)
    
    # Get repository info
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        repo_url = result.stdout.strip() if result.returncode == 0 else "Not configured"
    except:
        repo_url = "Not configured"
    
    print(f"📂 Repository: {repo_url}")
    print(f"🕐 Prepared at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Configuration: amplify.yml")
    print(f"⚙️  Environment: amplify_env_vars.json")
    
    print("\n🚀 Next Steps:")
    print("1. Push to GitHub:")
    print("   git add .")
    print("   git commit -m 'Prepare for Amplify deployment'")
    print("   git push origin main")
    print()
    print("2. Deploy via Amplify Console:")
    print("   • Go to: https://console.aws.amazon.com/amplify/")
    print("   • Click 'Get Started' under 'Deploy'")
    print("   • Connect your GitHub repository")
    print("   • Select 'main' branch")
    print("   • Build settings will be auto-detected from amplify.yml")
    print()
    print("3. Set Environment Variables:")
    print("   • Copy variables from amplify_env_vars.json")
    print("   • Add them in Amplify Console → Environment Variables")
    print()
    print("4. Deploy and Monitor:")
    print("   • Click 'Save and Deploy'")
    print("   • Monitor build progress in console")
    print("   • Your app will be live at: https://[app-id].amplifyapp.com")
    
    print("\n💡 Alternative: Deploy via Amplify CLI")
    print("   npm install -g @aws-amplify/cli")
    print("   amplify configure")
    print("   amplify init")
    print("   amplify add hosting")
    print("   amplify publish")

def main():
    """Main deployment preparation function."""
    print("🚀 AWS Amplify Deployment Preparation")
    print("=" * 60)
    
    # Check prerequisites
    issues = check_prerequisites()
    if issues:
        print("\n❌ Prerequisites not met:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 Fix these issues before proceeding with deployment.")
        return False
    
    # Validate dependencies
    if not validate_python_dependencies():
        print("\n💡 Update requirements.txt with missing dependencies.")
        return False
    
    # Create environment configuration
    env_config = create_amplify_environment_config()
    
    # Test application locally
    if not test_application_locally():
        print("\n💡 Fix application issues before deployment.")
        return False
    
    # Generate deployment summary
    generate_deployment_summary()
    
    print("\n🎉 Amplify deployment preparation complete!")
    print("📚 See AMPLIFY_DEPLOYMENT.md for detailed instructions.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)