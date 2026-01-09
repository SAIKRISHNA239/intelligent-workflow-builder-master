#!/bin/bash

# Intelligent Workflow Builder - Deployment Script
# This script helps deploy the application using Docker Compose

set -e  # Exit on error

echo "🚀 Intelligent Workflow Builder - Deployment Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${YELLOW}⚠️  Please edit .env file and add your API keys before continuing.${NC}"
        echo -e "${YELLOW}   Required: OPENAI_API_KEY${NC}"
        echo -e "${YELLOW}   Optional: GEMINI_API_KEY, SERPAPI_API_KEY${NC}"
        read -p "Press Enter after you've updated .env file..."
    else
        echo -e "${RED}❌ .env.example file not found. Please create .env file manually.${NC}"
        exit 1
    fi
fi

# Check if OPENAI_API_KEY is set
if ! grep -q "OPENAI_API_KEY=.*[^=]$" .env || grep -q "OPENAI_API_KEY=your_openai_api_key_here" .env; then
    echo -e "${RED}❌ OPENAI_API_KEY is not set in .env file.${NC}"
    echo -e "${YELLOW}   Please edit .env file and add your OpenAI API key.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Function to check if ports are available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${YELLOW}⚠️  Port $port is already in use${NC}"
        return 1
    fi
    return 0
}

# Check ports
echo "Checking if ports are available..."
check_port 3000 || echo -e "${YELLOW}   Frontend port 3000 is in use${NC}"
check_port 8000 || echo -e "${YELLOW}   Backend port 8000 is in use${NC}"
check_port 5433 || echo -e "${YELLOW}   PostgreSQL port 5433 is in use${NC}"
echo ""

# Ask user what to do
echo "What would you like to do?"
echo "1) Build and start services (first time)"
echo "2) Start existing services"
echo "3) Stop services"
echo "4) Restart services"
echo "5) View logs"
echo "6) Clean up (stop and remove containers)"
read -p "Enter choice [1-6]: " choice

case $choice in
    1)
        echo ""
        echo -e "${GREEN}🔨 Building and starting services...${NC}"
        docker-compose down -v 2>/dev/null || true
        docker-compose build --no-cache
        docker-compose up -d
        echo ""
        echo -e "${GREEN}✅ Services are starting...${NC}"
        echo ""
        echo "Waiting for services to be ready..."
        sleep 5
        docker-compose ps
        echo ""
        echo -e "${GREEN}🎉 Deployment complete!${NC}"
        echo ""
        echo "Access the application at:"
        echo "  Frontend: http://localhost:3000"
        echo "  Backend API: http://localhost:8000"
        echo "  API Docs: http://localhost:8000/docs"
        echo ""
        echo "To view logs: docker-compose logs -f"
        ;;
    2)
        echo ""
        echo -e "${GREEN}▶️  Starting services...${NC}"
        docker-compose start
        docker-compose ps
        ;;
    3)
        echo ""
        echo -e "${YELLOW}⏸️  Stopping services...${NC}"
        docker-compose stop
        echo -e "${GREEN}✅ Services stopped${NC}"
        ;;
    4)
        echo ""
        echo -e "${GREEN}🔄 Restarting services...${NC}"
        docker-compose restart
        docker-compose ps
        ;;
    5)
        echo ""
        echo -e "${GREEN}📋 Viewing logs (Press Ctrl+C to exit)...${NC}"
        docker-compose logs -f
        ;;
    6)
        echo ""
        read -p "⚠️  This will stop and remove all containers. Continue? [y/N]: " confirm
        if [[ $confirm == [yY] ]]; then
            echo -e "${YELLOW}🧹 Cleaning up...${NC}"
            docker-compose down
            echo -e "${GREEN}✅ Cleanup complete${NC}"
        else
            echo "Cancelled"
        fi
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
