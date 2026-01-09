# Cloud Deployment Guide 

### Option 1: Quick Testing with ngrok (Temporary Access)

**Best for**: Quick testing, demos, temporary access

```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com/

# Expose your local frontend
ngrok http 3000

# Expose your local backend
ngrok http 8000
```

**Pros**: 
- Free tier available
- Quick setup (5 minutes)
- Good for testing

**Cons**:
- Temporary URLs (change on restart)
- Requires your computer to be running
- Not suitable for production

---

### Option 2: Cloud Platform Deployment (Recommended for Production)

#### A. Railway.app (Easiest - Recommended)

**Best for**: Quick deployment, free tier available

1. **Sign up**: https://railway.app
2. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   ```
3. **Deploy**:
   ```bash
   cd /Users/krishna/Downloads/projects/intelligent-workflow-builder-master
   railway init
   railway up
   ```
4. **Add Environment Variables** in Railway dashboard:
   - `OPENAI_API_KEY`
   - `GEMINI_API_KEY` (optional)
   - `SERPAPI_API_KEY` (optional)
   - `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

**Cost**: Free tier available, then ~$5-20/month

---

#### B. Render.com (Easy - Good Free Tier)

**Best for**: Free tier, easy PostgreSQL setup

1. **Sign up**: https://render.com
2. **Create New Web Service**:
   - Connect your GitHub repo
   - Build command: `cd backend && pip install -r requirements.txt`
   - Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. **Create PostgreSQL Database** (free tier available)
4. **Create Static Site** for frontend:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/build`

**Cost**: Free tier available, then ~$7-25/month

---

#### C. Heroku (Popular but more expensive)

**Best for**: Established platform, good documentation

1. **Install Heroku CLI**:
   ```bash
   brew install heroku/brew/heroku
   heroku login
   ```
2. **Create apps**:
   ```bash
   heroku create your-app-backend
   heroku create your-app-frontend
   ```
3. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini -a your-app-backend
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

**Cost**: ~$7-25/month (no free tier anymore)

---

#### D. AWS (Most Flexible - More Complex)

**Best for**: Production, scalability, enterprise

**Services needed**:
- **EC2** or **ECS** for containers
- **RDS** for PostgreSQL
- **S3** for file storage
- **CloudFront** for CDN

**Cost**: Pay-as-you-go, ~$20-100/month depending on usage

---

#### E. Google Cloud Platform (GCP)

**Best for**: Integration with Google services

**Services**:
- **Cloud Run** for containers
- **Cloud SQL** for PostgreSQL
- **Cloud Storage** for files

**Cost**: Free tier available, then pay-as-you-go

---

#### F. DigitalOcean (Simple VPS)

**Best for**: Full control, simple pricing

1. **Create Droplet** (Ubuntu 22.04)
2. **Install Docker**:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```
3. **Clone and deploy**:
   ```bash
   git clone <your-repo>
   cd intelligent-workflow-builder-master
   docker-compose up -d
   ```

**Cost**: $6-12/month for basic droplet

---

### Option 3: VPS with Docker (Full Control)

**Best for**: Full control, custom domain

1. **Get a VPS** (DigitalOcean, Linode, Vultr, etc.)
2. **Install Docker** on the server
3. **Clone your project**
4. **Set up domain** (optional)
5. **Deploy with docker-compose**

---

## Recommended: Railway.app (Easiest Start)

Here's a step-by-step guide for Railway:

### Step 1: Prepare for Deployment

Create a `railway.json` or use their dashboard:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Environment Variables

Set these in Railway dashboard:
- `OPENAI_API_KEY` (required)
- `GEMINI_API_KEY` (optional)
- `SERPAPI_API_KEY` (optional)
- `POSTGRES_USER=workflow_user`
- `POSTGRES_PASSWORD=<generate-strong-password>`
- `POSTGRES_DB=workflow_db`
- `POSTGRES_HOST=<railway-postgres-host>`
- `POSTGRES_PORT=5432`
- `FRONTEND_URL=<your-frontend-url>`
- `BACKEND_URL=<your-backend-url>`

### Step 3: Deploy Frontend Separately

For frontend, you can:
1. Build static files: `npm run build`
2. Deploy to Railway, Vercel, or Netlify
3. Update `REACT_APP_API_URL` to point to your backend

---

## What You Need to Change for Cloud Deployment

### 1. Update CORS Settings

In `backend/app/core/config.py`, update CORS origins:

```python
CORS_ORIGINS: list = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",  # Add your cloud URL
    "https://*.railway.app",  # If using Railway
]
```

### 2. Update Frontend API URL

In `frontend/src/services/api.js` or environment variable:

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.com';
```

### 3. Database Configuration

Use cloud database (Railway Postgres, Render Postgres, etc.) instead of local.

### 4. File Storage

For production, consider:
- **AWS S3** for file uploads
- **Cloudinary** for media
- **Railway volumes** (persistent storage)

---
