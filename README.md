# Intelligent Workflow Builder - Full-Stack Application

A No-Code/Low-Code web application that enables users to visually create and interact with intelligent workflows. Users can configure a flow of components that handle user input, extract knowledge from documents, interact with language models, and return answers through a chat interface.

## 🏗️ Architecture Overview

The application consists of:
- **Frontend**: React.js with React Flow for visual workflow building
- **Backend**: FastAPI for RESTful API services
- **Database**: PostgreSQL for metadata and workflow storage
- **Vector Store**: ChromaDB for document embeddings
- **LLM Integration**: OpenAI GPT and Google Gemini
- **Web Search**: SerpAPI integration

## 📋 Core Components

1. **User Query Component**: Entry point that accepts user queries
2. **KnowledgeBase Component**: Handles document upload, text extraction, embedding generation, and vector search
3. **LLM Engine Component**: Processes queries with optional context and web search
4. **Output Component**: Displays responses in a chat interface

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)
- PostgreSQL 14+
- OpenAI API Key
- Google Gemini API Key (optional)
- SerpAPI Key (optional)

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
POSTGRES_USER=workflow_user
POSTGRES_PASSWORD=workflow_password
POSTGRES_DB=workflow_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google Gemini
GEMINI_API_KEY=your_gemini_api_key

# SerpAPI
SERPAPI_API_KEY=your_serpapi_key

# Application
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd assignment
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
assignment/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── models/              # Database models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic services
│   │   │   ├── llm_service.py   # LLM integration
│   │   │   ├── embedding_service.py  # Embedding generation
│   │   │   ├── vector_store.py  # ChromaDB operations
│   │   │   └── workflow_executor.py  # Workflow execution
│   │   ├── api/                 # API routes
│   │   └── core/                # Core configuration
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── hooks/               # Custom React hooks
│   │   └── utils/               # Utility functions
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🔧 Features

### Workflow Builder
- Drag-and-drop interface using React Flow
- Visual component connection
- Component configuration panel
- Workflow validation
- Zoom and pan support

### Document Processing
- PDF text extraction using PyMuPDF
- Automatic embedding generation
- Vector store integration
- Semantic search capabilities

### LLM Integration
- Support for OpenAI GPT models
- Support for Google Gemini
- Custom prompt configuration
- Optional web search integration

### Chat Interface
- Real-time query processing
- Workflow execution
- Response display
- Chat history (optional)

## 📡 API Endpoints

### Workflow Management
- `POST /api/workflows` - Create a new workflow
- `GET /api/workflows` - List all workflows
- `GET /api/workflows/{id}` - Get workflow details
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow

### Document Management
- `POST /api/documents/upload` - Upload and process document
- `GET /api/documents` - List all documents
- `DELETE /api/documents/{id}` - Delete document

### Workflow Execution
- `POST /api/workflows/{id}/execute` - Execute workflow with query

### Chat
- `POST /api/chat` - Send chat message through workflow

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🐳 Docker Deployment

### Build Images
```bash
docker-compose build
```

### Run Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
```

## ☸️ Kubernetes Deployment (Optional)

See `k8s/` directory for Kubernetes manifests and Helm charts.

## 📊 Monitoring (Optional)

- Prometheus metrics available at `/metrics`
- Grafana dashboards in `monitoring/` directory
- ELK Stack configuration in `logging/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is part of a technical assignment.

## 👤 Author

Edama Saikrishna

---

**Note**: This application requires API keys for OpenAI, Gemini, and SerpAPI to function fully. Please ensure you have valid API keys before running the application.

