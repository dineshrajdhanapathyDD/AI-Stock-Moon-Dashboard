# 🔧 AWS Amplify Deployment Troubleshooting

## 🚨 **Current Issues & Solutions**

### **Issue 1: YAML Parsing Errors**

**Error Message:**
```
CustomerError: Unable to parse build spec: the stream contains non-printable characters
CustomerError: The commands provided in the buildspec are malformed
```

**Root Cause:**
- Complex Python commands with colons and quotes in YAML
- Non-printable characters in build commands
- Improper YAML escaping

**✅ Solution:**
Use the simplified `amplify.yml` configuration:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - yum update -y
        - yum install -y python3 python3-pip python3-devel gcc
        - python3 -m pip install --upgrade pip
        - python3 -m pip install -r requirements.txt
    build:
      commands:
        - echo "Build completed"
  artifacts:
    baseDirectory: /
    files:
      - '**/*'
```

---

## 🔄 **Step-by-Step Fix Process**

### **Step 1: Update amplify.yml**
Replace the current `amplify.yml` with the minimal working version above.

### **Step 2: Commit and Push**
```bash
git add amplify.yml
git commit -m "Fix amplify.yml YAML formatting issues"
git push origin main
```

### **Step 3: Redeploy in Amplify Console**
1. Go to AWS Amplify Console
2. Select your app
3. Click "Redeploy this version" or trigger a new build

### **Step 4: Monitor Build Logs**
Watch for successful completion of:
- ✅ Pre-build phase (dependency installation)
- ✅ Build phase (basic validation)
- ✅ Artifact creation

---

## 🛠️ **Alternative Deployment Approaches**

### **Option A: Use Backend Configuration**
If frontend deployment continues to fail, try backend configuration:

```yaml
# amplify.yml
version: 1
backend:
  phases:
    preBuild:
      commands:
        - yum update -y
        - yum install -y python3 python3-pip python3-devel gcc
        - python3 -m pip install --upgrade pip
        - python3 -m pip install -r requirements.txt
    build:
      commands:
        - echo "Backend build completed"
  artifacts:
    baseDirectory: /
    files:
      - '**/*'
```

### **Option B: Manual Amplify CLI Deployment**
```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize project
amplify init

# Add hosting
amplify add hosting

# Deploy
amplify publish
```

### **Option C: Use Alternative Platforms**
If Amplify continues to have issues, deploy to:

**Render.com (Recommended Alternative):**
```bash
# Already configured with render.yaml
# Just connect GitHub repository to Render
```

**Railway:**
```bash
# Connect GitHub repository
# Auto-detects Python application
```

**Heroku:**
```bash
# Uses existing Procfile and runtime.txt
heroku create your-app-name
git push heroku main
```

---

## 🔍 **Debugging Commands**

### **Test Locally Before Deployment**
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('amplify.yml'))"

# Test application locally
python app.py

# Validate dependencies
pip install -r requirements.txt
```

### **Check Build Logs in Amplify**
1. Go to Amplify Console
2. Select your app
3. Click on failed build
4. Review detailed logs for specific errors

---

## 📋 **Working Environment Variables**

Set these in Amplify Console → Environment Variables:

```bash
PYTHONPATH=/opt/python
PORT=8050
DASH_DEBUG=False
DASH_HOST=0.0.0.0
DASH_COMPRESS=True
DASH_SERVE_LOCALLY=False
```

---

## 🎯 **Minimal Working Configuration**

**File: amplify.yml**
```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - yum update -y
        - yum install -y python3 python3-pip
        - pip3 install -r requirements.txt
    build:
      commands:
        - echo "Build complete"
  artifacts:
    baseDirectory: /
    files:
      - '**/*'
```

**File: requirements.txt** (ensure it exists and is valid)
```
dash>=2.14.0
plotly>=5.15.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
```

---

## 🚀 **Quick Deploy to Alternative Platform**

If Amplify issues persist, use Render.com for immediate deployment:

1. **Go to [Render.com](https://render.com)**
2. **Connect GitHub repository**
3. **Select `render.yaml` configuration**
4. **Deploy automatically**

The `render.yaml` is already configured and working.

---

## 📞 **Support Resources**

- **AWS Amplify Docs**: https://docs.amplify.aws/
- **YAML Validator**: https://yamlchecker.com/
- **Repository Issues**: Create issue in GitHub repository
- **Alternative Platforms**: Render, Railway, Heroku all configured

---

## ✅ **Success Checklist**

- [ ] `amplify.yml` uses minimal configuration
- [ ] No complex Python commands in build phase
- [ ] All quotes and colons properly escaped
- [ ] Environment variables set in Amplify Console
- [ ] Build logs show successful completion
- [ ] Application starts without errors

---

**🎯 Recommendation**: Use the minimal `amplify.yml` configuration above and set application testing to happen at runtime rather than build time. This avoids YAML parsing issues while still deploying successfully.