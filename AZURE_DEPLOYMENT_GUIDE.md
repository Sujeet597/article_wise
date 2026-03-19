# Azure App Service + GitHub Actions - Complete Deployment Guide

## 📋 Quick Fix for Your Current Issues

### Issue 1: GitHub Actions Build Failing (Exit Code 1)
**Solution:** The workflow is missing proper error handling and dependency installation.
**Fixed in:** `.github/workflows/deploy.yml`

### Issue 2: Azure Showing Old Code
**Solution:** Need to trigger redeployment and ensure proper startup configuration.
**Fixed in:** `startup.sh` and GitHub Actions workflow

### Issue 3: Port & Binding Issues
**Solution:** Streamlit needs specific configuration for Azure.
**Fixed in:** `startup.sh` and environment variables

---

## 🚀 Step 1: Create Azure Resources (One-time Setup)

### Option A: Using Azure Portal (GUI - Easiest)

1. **Create Resource Group**
   - Go to: https://portal.azure.com
   - Click "Resource groups" → "Create"
   - Name: `article-wise-rg`
   - Region: `East US` (or closest to you)
   - Click "Review + create"

2. **Create App Service Plan**
   - Click "Create a resource"
   - Search for "App Service Plan"
   - Fill in:
     - Name: `article-wise-plan`
     - Operating System: **Linux** ⚠️ Important
     - Region: Same as resource group
     - Sku: **B2** (minimum for Streamlit)
   - Click "Review + create"

3. **Create App Service**
   - In App Service Plan, click "Create app service"
   - Fill in:
     - Name: `article-wise-app`
     - Publish: **Code**
     - Runtime stack: **Python 3.11**
     - Operating System: **Linux**
   - Click "Review + create"

### Option B: Using Azure CLI (Command Line - Faster)

```bash
# Login to Azure
az login

# Create Resource Group
az group create \
  --name article-wise-rg \
  --location eastus

# Create App Service Plan (Linux)
az appservice plan create \
  --name article-wise-plan \
  --resource-group article-wise-rg \
  --sku B2 \
  --is-linux

# Create App Service
az webapp create \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --plan article-wise-plan \
  --runtime "python|3.11"
```

---

## 🔐 Step 2: Set Up GitHub Integration

### Step 2a: Get Publish Profile from Azure

1. Go to Azure Portal
2. Find your App Service: `article-wise-app`
3. Click "Download publish profile" (top right)
4. Save the file (it's XML)

### Step 2b: Add Publish Profile to GitHub Secrets

1. Go to GitHub: `https://github.com/Sujeet597/article_wise`
2. Click "Settings" (top right)
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
6. Value: Paste entire content of downloaded XML file
7. Click "Add secret"

---

## 📁 Step 3: Update Your Project Structure

Ensure your repository has these files:

```
article_wise/
├── .github/
│   └── workflows/
│       └── deploy.yml          ← GitHub Actions workflow
├── streamlit_app.py            ← Main app (required)
├── requirements.txt            ← Dependencies (required)
├── startup.sh                  ← Startup script (required)
├── web.config                  ← IIS config (required)
├── azure-config.ini            ← Azure settings (optional)
├── README.md
├── PROJECT_SUMMARY.md
├── config.py
└── ...other files
```

---

## 📤 Step 4: Push Files to GitHub

```bash
# Add all new files
git add .github/workflows/deploy.yml
git add startup.sh
git add web.config
git add azure-config.ini
git add requirements.txt

# Commit
git commit -m "Add Azure deployment configuration

- GitHub Actions workflow for CI/CD
- Startup script for Azure App Service
- Web.config for IIS integration
- Azure configuration settings
- Updated requirements.txt with pinned versions"

# Push to main branch (this triggers deployment)
git push origin main
```

---

## 🚀 Step 5: Monitor Your Deployment

### Watch GitHub Actions

1. Go to: `https://github.com/Sujeet597/article_wise/actions`
2. You should see a workflow running
3. Watch the build process:
   - ✅ Checkout code
   - ✅ Set up Python
   - ✅ Install dependencies
   - ✅ Deploy to Azure
4. Click workflow to see detailed logs

### Check Azure Deployment

1. Go to Azure Portal
2. Find your App Service: `article-wise-app`
3. Go to "Deployment slots" → "Logs"
4. Watch for: `✅ Deployment to Azure App Service completed`

### Verify App is Running

1. Wait 2-3 minutes for deployment
2. Go to: `https://article-wise-app.azurewebsites.net`
3. You should see your Streamlit app!

---

## 🔧 Step 6: Troubleshooting

### Build Fails with "Exit Code 1"

**Check logs:**
```bash
# In GitHub Actions, look for error in "Install dependencies" step
```

**Common causes:**
1. ❌ Missing `requirements.txt`
   → **Fix:** Add requirements.txt to repo

2. ❌ Invalid Python version
   → **Fix:** Use Python 3.9, 3.10, or 3.11

3. ❌ Missing dependency
   → **Fix:** Check requirements.txt has all packages

**Solution:**
```bash
# Verify locally first
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Azure Shows Old Code

**Cause:** App Service cache or no redeployment triggered

**Solution 1: Force redeployment**
```bash
# Go to Azure App Service
# → Configuration
# → Application settings
# → Add new setting
# → Name: DEPLOYMENT_ID
# → Value: <any-random-string>
# → Click "Save"
```

**Solution 2: Restart app service**
```bash
az webapp restart \
  --name article-wise-app \
  --resource-group article-wise-rg
```

**Solution 3: Redeploy from GitHub**
```bash
# Make a small commit and push
echo "# Trigger redeployment" >> README.md
git add README.md
git commit -m "Trigger redeployment"
git push origin main
```

### App Won't Start

**Check logs:**
```bash
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg
```

**Common issues:**
1. Port binding: Fixed in startup.sh ✅
2. Module not found: Check requirements.txt ✅
3. File permissions: startup.sh needs execute permission ✅

**Solution:**
```bash
# Make startup.sh executable
chmod +x startup.sh

# Commit and push
git add startup.sh
git commit -m "Fix startup script permissions"
git push origin main
```

### Deployment Takes Too Long

Normal deployment time: 3-5 minutes

**If taking longer:**
1. Wait up to 10 minutes (first deployment is slower)
2. Check Azure logs for errors
3. Restart if stuck: Use Azure Portal or CLI

### 502 Bad Gateway Error

**Cause:** App is starting but not responding

**Solutions:**
1. Wait 1-2 more minutes (app still starting)
2. Check logs for errors
3. Verify port configuration (should be 8000)
4. Check requirements.txt is installed

---

## ⚙️ Step 7: Configure Azure App Service Settings

### Via Azure Portal

1. Go to your App Service
2. Click "Configuration"
3. Click "Application settings"
4. Add these settings:

```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_CLIENT_TOOLBAR_MODE=minimal
PYTHONUNBUFFERED=1
WEBSITES_PORT=8000
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

5. Click "Save"
6. Your app will restart

### Via Azure CLI

```bash
az webapp config appsettings set \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --settings \
  STREAMLIT_SERVER_HEADLESS=true \
  STREAMLIT_CLIENT_TOOLBAR_MODE=minimal \
  PYTHONUNBUFFERED=1 \
  WEBSITES_PORT=8000 \
  SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

---

## 🔄 Step 8: Set Up Continuous Deployment

### Automatic Deployment on Every Push

✅ Already configured in `.github/workflows/deploy.yml`

Every time you push to `main` branch:
1. GitHub Actions builds your app
2. Tests are run (if any)
3. App is deployed to Azure
4. Health check runs
5. You get status in GitHub

### Trigger Manual Deployment

**Option 1: GitHub Actions**
- Go to Actions tab
- Click workflow
- Click "Run workflow"
- Select branch (main)
- Click "Run workflow"

**Option 2: Azure CLI**
```bash
# Restart app service
az webapp restart \
  --name article-wise-app \
  --resource-group article-wise-rg
```

**Option 3: Git Push**
```bash
# Any commit to main triggers deployment
git commit --allow-empty -m "Trigger redeployment"
git push origin main
```

---

## 📊 Step 9: Monitor Your Application

### View Live Logs

```bash
# Tail logs in real-time
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg

# Download logs
az webapp log download \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --log-file logs.zip
```

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app article-wise-insights \
  --location eastus \
  --resource-group article-wise-rg \
  --application-type web

# Link to App Service
az webapp config appsettings set \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --settings \
  APPINSIGHTS_INSTRUMENTATIONKEY=<key>
```

---

## 🔐 Security Best Practices

### 1. Enable HTTPS Only
```bash
az webapp update \
  --name article-wise-app \
  --resource-group article-wise-rg \
  --https-only
```

### 2. Set IP Restrictions (Optional)
```bash
az webapp config access-restriction add \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --rule-name AllowOffice \
  --priority 100 \
  --ip-address <YOUR-IP>/32
```

### 3. Enable Authentication (Optional)
See Azure AD authentication documentation

### 4. Rotate Secrets Regularly
- Update publish profile every 6 months
- Regenerate deployment credentials
- Rotate API keys if any

---

## 💰 Cost Optimization

### For Development/Testing
Use **B1 tier** instead of B2:
- Lower cost (~$10-15/month)
- Sufficient for testing

### For Production
Use **B2 or P1V2 tier**:
- Better performance
- Always On enabled
- Cost: $50-100+/month

### Cost Estimation
- B2: ~$50/month
- 1 GB file uploads: ~$0.12 per GB
- Outbound data: Varies by volume

---

## 🆘 Quick Reference

### Environment Variables (All Required)
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_PORT=8000
PYTHONUNBUFFERED=1
```

### Key Files
```
.github/workflows/deploy.yml  → GitHub Actions workflow
startup.sh                    → App startup command
web.config                    → IIS configuration
requirements.txt              → Python dependencies
azure-config.ini              → Azure settings reference
```

### Useful URLs
```
GitHub Repo:     https://github.com/Sujeet597/article_wise
Azure Portal:    https://portal.azure.com
App URL:         https://article-wise-app.azurewebsites.net
Actions:         https://github.com/Sujeet597/article_wise/actions
```

### Useful Commands
```bash
# Login to Azure
az login

# Check deployment status
az webapp deployment show \
  --name article-wise-app \
  --resource-group article-wise-rg

# View live logs
az webapp log tail \
  --name article-wise-app \
  --resource-group article-wise-rg

# Restart app
az webapp restart \
  --name article-wise-app \
  --resource-group article-wise-rg

# Update settings
az webapp config appsettings set \
  --resource-group article-wise-rg \
  --name article-wise-app \
  --settings KEY=VALUE
```

---

## ✅ Deployment Checklist

Before pushing to GitHub:

- [ ] `streamlit_app.py` exists
- [ ] `requirements.txt` has all dependencies
- [ ] `startup.sh` is in repo
- [ ] `web.config` is in repo
- [ ] `.github/workflows/deploy.yml` exists
- [ ] GitHub secret `AZURE_WEBAPP_PUBLISH_PROFILE` is set
- [ ] Azure App Service created (Linux, Python 3.11)
- [ ] App Service name is `article-wise-app`
- [ ] Resource group is `article-wise-rg`

---

## 🎉 Success!

If everything is configured correctly:

1. Push code to `main` branch
2. GitHub Actions automatically builds and deploys
3. Azure deploys your app
4. Access at: `https://article-wise-app.azurewebsites.net`
5. Check logs if anything fails

---

## 📞 Support

**GitHub Issues:**
- Go to: https://github.com/Sujeet597/article_wise/issues
- Describe the problem
- Share error logs

**Azure Support:**
- Go to: https://portal.azure.com → Help + support
- Create support request
- Provide subscription and app name

---

## 📚 Additional Resources

- Streamlit Deployment: https://docs.streamlit.io/deploy/overview
- Azure App Service: https://learn.microsoft.com/azure/app-service/
- GitHub Actions: https://docs.github.com/actions
- Python on Azure: https://azure.microsoft.com/python/

---

**Your app is now production-ready on Azure! 🚀**
