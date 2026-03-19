# Streamlit App - Deployment Guide

Deploy your MSA Article Stock Analysis web app to the cloud or local network.

## 🎯 Quick Deployment Options

| Option | Time | Cost | Difficulty | Best For |
|--------|------|------|------------|----------|
| **Local** | 2 min | Free | ⭐ Easy | Development, testing |
| **Network Share** | 3 min | Free | ⭐ Easy | Team on same network |
| **Streamlit Cloud** | 5 min | Free | ⭐⭐ Easy | Quick cloud deployment |
| **Docker Local** | 10 min | Free | ⭐⭐⭐ Medium | Consistent environments |
| **AWS EC2** | 15 min | $$ | ⭐⭐⭐ Medium | Production use |
| **Heroku** | 10 min | $$ | ⭐⭐⭐ Medium | Simple cloud app |

---

## 1️⃣ Local Deployment (FASTEST)

Perfect for your own computer or team testing.

### Install & Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Access:** `http://localhost:8501`

**Pros:**
- ✅ No configuration needed
- ✅ Free
- ✅ Fastest setup

**Cons:**
- ❌ Only works on your computer
- ❌ App stops when you close terminal

---

## 2️⃣ Network Deployment (For Teams)

Share the app across your local network.

### Run on Network
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

### Access from Other Computers
```
http://<YOUR-IP-ADDRESS>:8501
```

**Find your IP address:**
- **Windows:** Open Command Prompt, type `ipconfig`
- **Mac/Linux:** Open Terminal, type `hostname -I`

**Example:** `http://192.168.1.100:8501`

**Pros:**
- ✅ Free
- ✅ Easy to share with team
- ✅ Works on same network

**Cons:**
- ❌ Only works on local network
- ❌ App stops when you close terminal

---

## 3️⃣ Streamlit Cloud (EASIEST CLOUD)

Host on Streamlit's free cloud platform.

### Step 1: Push to GitHub

```bash
git add streamlit_app.py requirements.txt
git commit -m "Add Streamlit web app"
git push origin main
```

### Step 2: Create Streamlit Cloud Account

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "Create app"

### Step 3: Deploy

1. Select your repository
2. Select branch: `main`
3. Select file path: `streamlit_app.py`
4. Click "Deploy"

**That's it!** Your app is live at: `https://<your-username>-<project>-<random>.streamlit.app`

**Pros:**
- ✅ Completely free
- ✅ Easy to share (just send URL)
- ✅ HTTPS included
- ✅ Auto-deploys on GitHub push

**Cons:**
- ⚠️ Free tier has usage limits
- ⚠️ Requires GitHub account
- ⚠️ Apps go to sleep after 1 hour inactivity

**Cost:** Free (with paid options starting at $5/month)

---

## 4️⃣ Docker Deployment (PROFESSIONAL)

Package your app in Docker for consistent deployment.

### Step 1: Create Dockerfile

Create a file named `Dockerfile` (no extension):

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_app.py .
COPY PROJECT_SUMMARY.md .
COPY STREAMLIT_README.md .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

### Step 2: Build Docker Image

```bash
docker build -t msa-app:1.0 .
```

### Step 3: Run Container

```bash
docker run -p 8501:8501 msa-app:1.0
```

**Access:** `http://localhost:8501`

**Pros:**
- ✅ Consistent across all machines
- ✅ Easy to scale
- ✅ Professional approach

**Cons:**
- ❌ Requires Docker installation
- ❌ Slightly more complex

---

## 5️⃣ AWS EC2 Deployment

Host on Amazon's cloud infrastructure.

### Prerequisites
- AWS account (free tier available)
- EC2 instance running Ubuntu

### Step 1: Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### Step 2: Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```

### Step 3: Run App

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 80
```

### Step 4: Configure Security Group

1. Go to AWS Console
2. Find your instance
3. Edit Security Group
4. Allow inbound traffic on port 80

**Access:** `http://your-instance-ip`

**Cost:** Free tier eligible (12 months free), then $0.0116/hour minimum

---

## 6️⃣ Heroku Deployment (SIMPLE PAID)

Simple cloud deployment platform.

### Step 1: Create Heroku Account

Go to https://www.heroku.com and sign up.

### Step 2: Create Procfile

Create a file named `Procfile`:

```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 3: Push to Heroku

```bash
heroku create msa-app
git push heroku main
heroku logs --tail
```

**Access:** `https://msa-app.herokuapp.com`

**Cost:** Free tier deprecated, but plans start at $7/month

---

## 7️⃣ PythonAnywhere Deployment

Simple Python hosting platform.

### Step 1: Create Account

Go to https://www.pythonanywhere.com and sign up (free tier available).

### Step 2: Upload Files

1. Go to "Files"
2. Create new directory: `msa-app`
3. Upload `streamlit_app.py` and `requirements.txt`

### Step 3: Install Dependencies

```bash
pip3.9 install -r requirements.txt --user
```

### Step 4: Create Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Choose Python 3.9
5. Point to your Streamlit app

---

## 🚀 Recommended Setup

**For Testing:**
→ Use **Local Deployment** (1-2 minutes)

**For Team Use:**
→ Use **Network Deployment** (2-3 minutes)

**For Production (Free):**
→ Use **Streamlit Cloud** (5 minutes)

**For Production (Paid, Professional):**
→ Use **Docker + AWS EC2** (20-30 minutes)

---

## 📊 Performance Tips

**For Large Datasets:**

1. **Increase Server Resources**
   ```bash
   streamlit run streamlit_app.py --client.maxMessageSize=200
   ```

2. **Enable Caching**
   - Already included in streamlit_app.py
   - Speeds up repeated file uploads

3. **Use CSVs**
   - Faster than Excel for large files
   - Take up less memory

---

## 🔒 Security Considerations

**For Production Deployment:**

1. **Use HTTPS**
   - Enable on your cloud provider
   - Never expose HTTP ports to internet

2. **Limit File Uploads**
   - Maximum file size: 200 MB default
   - Configure in Streamlit config if needed

3. **Add Authentication** (Optional)
   ```bash
   pip install streamlit-authenticator
   ```

4. **Hide Credentials**
   - Never commit API keys
   - Use environment variables
   - Use `.gitignore`

---

## 🛠️ Configuration Files

### streamlit/config.toml

Create `.streamlit/config.toml` for custom settings:

```toml
[server]
maxUploadSize = 200
port = 8501

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
maxMessageSize = 200
```

### .streamlit/secrets.toml

For API keys (don't commit to GitHub):

```toml
# Example - Not needed for this app
api_key = "your-secret-key"
```

Add to `.gitignore`:
```
.streamlit/secrets.toml
```

---

## 📈 Monitoring & Logs

**Local Logs:**
```bash
streamlit run streamlit_app.py --logger.level=debug
```

**Cloud Logs:**
- Streamlit Cloud: Dashboard shows logs
- Heroku: `heroku logs --tail`
- AWS: CloudWatch dashboard
- Docker: `docker logs container-id`

---

## 🆘 Troubleshooting

**App won't start:**
```bash
pip install -r requirements.txt --upgrade
```

**Port already in use:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

**Memory issues:**
- Reduce uploaded file sizes
- Process smaller batches
- Use a more powerful machine

**Slow performance:**
- Check internet speed
- Use SSD storage
- Enable caching (already done)

---

## 📚 More Resources

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud: https://streamlit.io/cloud
- AWS Docs: https://aws.amazon.com/documentation
- Docker Docs: https://docs.docker.com
- Heroku Docs: https://devcenter.heroku.com

---

## Summary

**Choose your deployment:**
1. Testing → **Local** (2 min)
2. Team → **Network** (3 min)
3. Production → **Streamlit Cloud** (5 min)
4. Enterprise → **AWS + Docker** (30 min)

**Next:** Pick one and deploy! 🚀
