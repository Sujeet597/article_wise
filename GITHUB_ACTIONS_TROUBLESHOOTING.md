# GitHub Actions + Azure Deployment - Troubleshooting Guide

## 🔍 Common Build Failures and Solutions

### 1. Exit Code 1 - General Build Failure

**Error Message:**
```
The job failed with exit code 1
```

**Root Causes & Solutions:**

#### 1a. Missing requirements.txt
```bash
# Error: No such file or directory: requirements.txt

# Solution:
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

#### 1b. Python Version Incompatibility
```bash
# Error: Python 3.8 not supported by streamlit

# Solution in .github/workflows/deploy.yml:
python-version: '3.11'  # Change from 3.8 to 3.11
```

#### 1c. Dependency Installation Failure
```bash
# Error: Could not find version of 'pandas' matching requirement

# Solution - Fix requirements.txt:
pandas>=2.0.0,<3.0.0  # Add version constraints
streamlit>=1.28.0,<2.0.0
```

#### 1d. Permission Denied (startup.sh)
```bash
# Error: Permission denied: ./startup.sh

# Solution:
git update-index --chmod=+x startup.sh
git commit -m "Fix startup.sh permissions"
git push origin main
```

---

### 2. Build Succeeds But Deployment Fails

**Error in Azure:**
```
Deployment failed. Exit code: 1
```

**Solutions:**

#### 2a. Check Publish Profile
```bash
# Verify secret exists:
# Go to GitHub → Settings → Secrets → AZURE_WEBAPP_PUBLISH_PROFILE

# If missing:
# 1. Download new publish profile from Azure Portal
# 2. Go to GitHub Settings → Secrets
# 3. Update AZURE_WEBAPP_PUBLISH_PROFILE
```

#### 2b. Verify App Service Name
```yaml
# In .github/workflows/deploy.yml
env:
  AZURE_WEBAPP_NAME: article-wise-app  # Match your Azure app name exactly
```

#### 2c. Check Web.config
```bash
# web.config is required for Windows App Service
# For Linux App Service, startup.sh is used instead

# Ensure web.config has:
# - httpPlatform processPath configured
# - environmentVariables set correctly
# - requestLimits adjusted for uploads
```

---

### 3. Deployment Succeeds But App Doesn't Start

**Symptoms:**
- 502 Bad Gateway
- 503 Service Unavailable
- App keeps restarting

**Solutions:**

#### 3a. Check Port Configuration
```bash
# Error: Address already in use: 0.0.0.0:8000

# Solution - Verify startup.sh:
export STREAMLIT_SERVER_PORT=${WEBSITES_PORT:-8000}
export STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Check Azure settings:
# Configuration → Application Settings
# WEBSITES_PORT = 8000
```

#### 3b. Check Streamlit Module
```bash
# Error: ModuleNotFoundError: No module named 'streamlit'

# Solution:
# 1. Add to requirements.txt:
streamlit>=1.28.0,<2.0.0

# 2. Verify in workflow:
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    streamlit --version  # This should work
```

#### 3c. Check Python Path
```bash
# Error: python: command not found

# Solution in startup.sh:
#!/bin/bash  # Must be bash, not sh
set -e      # Exit on error

python --version  # Verify Python is available
```

---

### 4. Old Code Still Showing After Deployment

**Cause:**
- Azure cache not cleared
- Deployment slot not updated
- App restart didn't occur

**Solutions:**

#### 4a. Force Redeployment
```bash
# Option 1: Restart App Service
az webapp restart \
  --name article-wise-app \
  --resource-group article-wise-rg

# Option 2: Add deployment trigger
git commit --allow-empty -m "Force redeployment"
git push origin main

# Option 3: Update app setting to trigger restart
az webapp config appsettings set \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --settings DEPLOYMENT_ID=$(date +%s)
```

#### 4b: Clear Cache
```bash
# Via Azure Portal:
# App Service → Configuration → General Settings
# → Stack settings → Check for cache options
# → Save (this restarts the app)
```

#### 4c: Check Deployment Logs
```bash
# View detailed deployment logs
az webapp deployment log show \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --slot production
```

---

### 5. File Upload Size Limit Exceeded

**Error:**
```
413 Payload Too Large
```

**Solution:**

#### 5a: Update requirements.txt
```python
# Ensure limits are set in web.config:
<requestLimits maxAllowedContentLength="209715200" />
# This is 200MB limit
```

#### 5b: Set App Setting in Azure
```bash
az webapp config appsettings set \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --settings \
  SCRIPT_DEBUG=1 \
  ENABLE_ORYX_BUILD=true
```

---

## 🛠️ Advanced Debugging

### Enable GitHub Actions Debug Logging

```yaml
# Add to workflow step:
- name: Enable debug
  run: |
    set -x  # Enable debug mode
    echo "Debug enabled"
```

### Enable Azure Deployment Logs

```bash
# Stream logs in real-time
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --provider Application

# Get all logs
az webapp log download \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --log-file app-logs.zip
```

### Test Locally Before Pushing

```bash
# Test GitHub Actions locally with act
# https://github.com/nektos/act

# Install
brew install act

# Run workflow locally
act -j build

# Run deployment job
act -j deploy
```

---

## 📋 Diagnostic Steps

### Step 1: Check GitHub Actions Logs

1. Go to GitHub Actions tab
2. Click on failed workflow
3. Expand each step to see output
4. Look for red ❌ errors
5. Check stdout/stderr carefully

### Step 2: Check Azure Logs

```bash
# Connect to Azure
az login

# Stream app logs
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg
```

### Step 3: Test App Locally

```bash
# Clone repo
git clone https://github.com/Sujeet597/article_wise.git
cd article_wise

# Create venv
python -m venv venv
source venv/bin/activate

# Install deps
pip install -r requirements.txt

# Run app
streamlit run streamlit_app.py
```

### Step 4: Verify Azure Configuration

```bash
# Check app settings
az webapp config appsettings list \
  --name article-wise-app \
  --resource-group article-wise-rg

# Check runtime settings
az webapp config show \
  --name article-wise-app \
  --resource-group article-wise-rg
```

---

## 🔧 Common Configuration Issues

### Issue: CORS Error in Browser Console
```javascript
// Error: Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution in startup.sh:**
```bash
export STREAMLIT_SERVER_ENABLECORS=false
# Or in .streamlit/config.toml:
[server]
enableCORS = false
```

### Issue: WebSocket Connection Failed
```javascript
// Error: WebSocket connection to ... failed
```

**Solution in web.config:**
```xml
<webSocket enabled="true" />
```

### Issue: Large File Upload Timeout
```
ERR_INCOMPLETE_CHUNKED_ENCODING
```

**Solution:**
```bash
# Increase timeout in startup.sh
export STREAMLIT_CLIENT_MAX_MESSAGE_SIZE=200
```

---

## 📊 Performance Issues

### App Running Slowly

```bash
# 1. Check app size
du -sh ~/.streamlit/
du -sh venv/

# 2. Check Azure App Service plan
az appservice plan show \
  --name article-wise-plan \
  --resource-group article-wise-rg \
  --query sku

# 3. Upgrade if needed
az appservice plan update \
  --name article-wise-plan \
  --resource-group article-wise-rg \
  --sku P1V2  # More powerful
```

### Memory Issues

```bash
# In startup.sh, add memory limit monitoring:
echo "Memory available: $(free -h)"

# Check Python memory usage
python -c "import os; print(os.popen('ps aux | grep streamlit').read())"
```

---

## 🚀 Optimization Tips

### 1. Cache Dependencies

The workflow already includes:
```yaml
- uses: actions/setup-python@v4
  with:
    cache: 'pip'  # This caches pip packages
```

### 2. Optimize Image Size

```dockerfile
# Use slim Python image
FROM python:3.11-slim

# Install only required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
```

### 3. Parallel Builds

Current workflow is sequential. For future optimization:
```yaml
strategy:
  matrix:
    python-version: [3.9, '3.10', 3.11]
```

---

## 📝 Workflow File Explanation

```yaml
name: Deploy Streamlit to Azure App Service
# Workflow name shown in GitHub

on:
  push:
    branches: [main, develop]
  # Triggers on push to main or develop

env:
  AZURE_WEBAPP_NAME: article-wise-app
  # Set once, use throughout workflow

jobs:
  build:
    runs-on: ubuntu-latest
    # Run on latest Ubuntu runner

    steps:
    - uses: actions/checkout@v3
      # Clone your repo

    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
      # Install Python 3.11

    - run: pip install -r requirements.txt
      # Install dependencies

    - uses: azure/webapps-deploy@v2
      # Deploy to Azure
```

---

## ✅ Pre-Deployment Checklist

- [ ] `requirements.txt` exists and installs locally
- [ ] `streamlit_app.py` runs with `streamlit run streamlit_app.py`
- [ ] `startup.sh` is executable: `chmod +x startup.sh`
- [ ] `web.config` has correct httpPlatform settings
- [ ] `.github/workflows/deploy.yml` exists
- [ ] GitHub secret `AZURE_WEBAPP_PUBLISH_PROFILE` is set
- [ ] Azure App Service created with Python 3.11
- [ ] Azure App Service name matches workflow file
- [ ] Port 8000 is not blocked
- [ ] All files committed to git: `git status`

---

## 🎯 Deployment Success Criteria

✅ **Build Succeeded**
- No red ❌ in GitHub Actions
- "Build completed" message
- Artifacts uploaded

✅ **Deployment Succeeded**
- "Deployment to Azure App Service initiated" message
- No deployment errors in Azure logs

✅ **App Running**
- No 502/503 errors
- Page loads at https://article-wise-app.azurewebsites.net
- Can upload files and process data

✅ **Health Check Passed**
- HTTP 200 or 302 response
- App is healthy

---

## 💡 Quick Tips

**Tip 1: Speed up rebuilds**
- The workflow caches pip packages
- Subsequent builds are faster

**Tip 2: Debug without pushing**
- Test locally first
- Use `streamlit run streamlit_app.py` locally

**Tip 3: Check before committing**
```bash
# Verify all files exist
ls startup.sh web.config requirements.txt streamlit_app.py

# Check startup.sh is executable
file startup.sh

# Test requirements.txt locally
pip install -r requirements.txt
```

**Tip 4: Monitor deployments**
```bash
# Watch Azure logs while workflow runs
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg \
  -f
```

---

## 📞 Need More Help?

1. **Check workflow logs:** GitHub Actions tab → Failed workflow
2. **Check Azure logs:** Azure Portal → Logs → Application logs
3. **Test locally:** `streamlit run streamlit_app.py`
4. **Verify setup:** Follow AZURE_DEPLOYMENT_GUIDE.md

---

**Your deployment is now fully optimized! 🎉**
