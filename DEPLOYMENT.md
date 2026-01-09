# Deployment Guide - Intelligent Workflow Builder

This guide will help you deploy the Intelligent Workflow Builder application using Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- OpenAI API Key (required)
- Optional: Gemini API Key, SerpAPI Key

## Quick Start Deployment

### Step 1: Clone and Navigate to Project

```bash
cd /Users/krishna/Downloads/projects/intelligent-workflow-builder-master
```

### Step 2: Create Environment File

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:

```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
GEMINI_API_KEY=your-gemini-key-here  # Optional
SERPAPI_API_KEY=your-serpapi-key-here  # Optional
```

### Step 3: Build and Start Services

```bash
docker-compose up --build -d
```

The `-d` flag runs containers in detached mode (background).

### Step 4: Check Service Status

```bash
docker-compose ps
```

You should see all three services running:
- `workflow_postgres` (PostgreSQL database)
- `workflow_backend` (FastAPI backend)
- `workflow_frontend` (React frontend)

### Step 5: View Logs

To see logs from all services:

```bash
docker-compose logs -f
```

To see logs from a specific service:

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Step 6: Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Service Management

### Stop Services

```bash
docker-compose stop
```

### Start Services (after stopping)

```bash
docker-compose start
```

### Restart Services

```bash
docker-compose restart
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Stop and Remove Containers + Volumes (⚠️ This deletes data)

```bash
docker-compose down -v
```

## Troubleshooting

### Check if ports are already in use

```bash
# Check port 3000 (frontend)
lsof -i :3000

# Check port 8000 (backend)
lsof -i :8000

# Check port 5433 (postgres)
lsof -i :5433
```

If ports are in use, you can modify them in `docker-compose.yml`.

### View Backend Logs for Errors

```bash
docker-compose logs backend | tail -50
```

### Restart a Specific Service

```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres
```

### Rebuild a Specific Service

```bash
docker-compose build backend
docker-compose up -d backend
```

### Database Connection Issues

If the backend can't connect to the database:

1. Check if postgres is healthy:
```bash
docker-compose ps postgres
```

2. Check postgres logs:
```bash
docker-compose logs postgres
```

3. Restart postgres:
```bash
docker-compose restart postgres
```

### Frontend Not Loading

1. Check if frontend is running:
```bash
docker-compose ps frontend
```

2. Check frontend logs:
```bash
docker-compose logs frontend
```

3. Rebuild frontend:
```bash
docker-compose build frontend
docker-compose up -d frontend
```

## Production Deployment Considerations

### 1. Environment Variables

For production, use secure methods to manage environment variables:
- Use Docker secrets
- Use a secrets management service (AWS Secrets Manager, HashiCorp Vault, etc.)
- Never commit `.env` files to version control

### 2. Database Backups

Set up regular backups for PostgreSQL:

```bash
# Backup database
docker-compose exec postgres pg_dump -U workflow_user workflow_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U workflow_user workflow_db < backup.sql
```

### 3. SSL/HTTPS

For production, set up:
- Reverse proxy (nginx, Traefik)
- SSL certificates (Let's Encrypt)
- Update CORS settings in `backend/app/core/config.py`

### 4. Resource Limits

Add resource limits to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 5. Health Checks

The services include health checks. Monitor them:

```bash
docker-compose ps
```

## Monitoring

### Check Service Health

```bash
# All services
docker-compose ps

# Backend health endpoint
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres pg_isready -U workflow_user
```

### View Resource Usage

```bash
docker stats
```

## Updating the Application

### Pull Latest Changes

```bash
git pull origin main
```

### Rebuild and Restart

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Data Persistence

Data is persisted in Docker volumes:
- `postgres_data`: Database data
- `uploads_data`: Uploaded documents
- `chroma_data`: Vector database (ChromaDB)

To backup volumes:

```bash
docker run --rm -v intelligent-workflow-builder-master_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

## Clean Up

### Remove All Containers and Volumes

⚠️ **Warning**: This will delete all data!

```bash
docker-compose down -v
docker system prune -a
```

## Support

If you encounter issues:

1. Check logs: `docker-compose logs -f`
2. Verify environment variables: `docker-compose config`
3. Check service status: `docker-compose ps`
4. Review this guide's troubleshooting section
