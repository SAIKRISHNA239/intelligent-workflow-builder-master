# Architecture Overview

## System Architecture

The Intelligent Workflow Builder is a full-stack application that enables users to visually create and execute intelligent workflows using a no-code/low-code interface.

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Workflow     │  │ Component    │  │ Chat        │      │
│  │ Builder      │  │ Config Panel │  │ Interface   │      │
│  │ (React Flow) │  │              │  │             │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
┌───────────────────────────┴─────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Workflow     │  │ Document     │  │ Execution    │      │
│  │ Management   │  │ Processing   │  │ Engine       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ LLM Service  │  │ Embedding    │  │ Vector      │      │
│  │ (OpenAI/     │  │ Service      │  │ Store       │      │
│  │  Gemini)     │  │              │  │ (ChromaDB)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────┴────────┐                    ┌───────┴────────┐
│  PostgreSQL    │                    │   ChromaDB     │
│  (Metadata)    │                    │  (Embeddings)  │
└────────────────┘                    └────────────────┘
```

## Component Flow

### Workflow Execution Flow

```
User Query
    │
    ▼
[User Query Component]
    │
    ├───► [KnowledgeBase Component] ──► [Vector Search] ──► Context
    │                                                           │
    │                                                           ▼
    └─────────────────────────────────────────────────────► [LLM Engine]
                                                                 │
                                                                 ├───► [Web Search] (Optional)
                                                                 │
                                                                 ▼
                                                            [Output Component]
                                                                 │
                                                                 ▼
                                                            Chat Response
```

## Technology Stack

### Frontend
- **React 18**: UI framework
- **React Flow**: Drag-and-drop workflow builder
- **Axios**: HTTP client
- **CSS3**: Styling

### Backend
- **FastAPI**: REST API framework
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Pydantic**: Data validation

### Database & Storage
- **PostgreSQL**: Relational database for metadata
- **ChromaDB**: Vector database for embeddings

### AI/ML Services
- **OpenAI API**: GPT models and embeddings
- **Google Gemini API**: Alternative LLM and embeddings
- **SerpAPI**: Web search integration

### Text Processing
- **PyMuPDF**: PDF text extraction

## Data Models

### Workflow
- Stores workflow definitions
- Contains components and connections
- Links to chat sessions

### WorkflowComponent
- Represents a component in the workflow
- Stores component type, position, and configuration
- Linked to workflow via foreign key

### ComponentConnection
- Defines connections between components
- Stores source and target component IDs
- Includes handle information for React Flow

### Document
- Stores document metadata
- Tracks processing status
- Links to knowledgebase components

### ChatMessage
- Stores chat history
- Links to workflows and sessions
- Contains execution metadata

## API Endpoints

### Workflows
- `POST /api/workflows` - Create workflow
- `GET /api/workflows` - List workflows
- `GET /api/workflows/{id}` - Get workflow
- `PUT /api/workflows/{id}` - Update workflow
- `DELETE /api/workflows/{id}` - Delete workflow
- `POST /api/workflows/{id}/validate` - Validate workflow
- `POST /api/workflows/{id}/execute` - Execute workflow

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents` - List documents
- `GET /api/documents/{id}` - Get document
- `DELETE /api/documents/{id}` - Delete document

### Chat
- `POST /api/chat` - Send message
- `GET /api/chat/sessions/{session_id}` - Get chat history
- `GET /api/chat/workflows/{workflow_id}/sessions` - List sessions

## Security Considerations

- API keys stored in environment variables
- CORS configured for frontend origin
- File upload size limits
- Input validation on all endpoints
- SQL injection prevention via ORM

## Deployment Architecture

### Docker Compose
- Frontend container (React)
- Backend container (FastAPI)
- PostgreSQL container
- Shared network for communication

### Optional Kubernetes
- Deployment manifests for each service
- Service definitions
- ConfigMaps for configuration
- Persistent volumes for data

## Scalability Considerations

- Stateless backend design
- Database connection pooling
- Vector store can be scaled horizontally
- Frontend can be served via CDN
- API can be load balanced

## Future Enhancements

- User authentication and authorization
- Workflow templates
- Real-time collaboration
- Advanced workflow scheduling
- Performance monitoring and analytics
- Multi-tenant support

