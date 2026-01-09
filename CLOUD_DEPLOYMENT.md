# Cloud Deployment Guide 

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
