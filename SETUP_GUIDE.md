# Setup Guide - Intelligent Workflow Builder

This guide will help you set up and run the Intelligent Workflow Builder application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose** (recommended)
  OR
- **Node.js** 18+ and **Python** 3.10+ (for local development)
- **PostgreSQL** 14+ (if not using Docker)
- API Keys:
  - OpenAI API Key (required)
  - Google Gemini API Key (optional)
  - SerpAPI Key (optional, for web search)

## Quick Start with Docker (Recommended)

1. **Clone the repository** (if applicable) or navigate to the project directory:
   ```bash
   cd assignment
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env` file** and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here  # Optional
   SERPAPI_API_KEY=your_serpapi_key_here    # Optional
   ```

4. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   Create a `.env` file in the `backend` directory:
   ```env
   POSTGRES_USER=workflow_user
   POSTGRES_PASSWORD=workflow_password
   POSTGRES_DB=workflow_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   SERPAPI_API_KEY=your_serpapi_key_here
   ```

6. **Set up PostgreSQL database**:
   - Create a PostgreSQL database
   - Update the connection details in `.env`

7. **Run database migrations** (if using Alembic):
   ```bash
   alembic upgrade head
   ```
   Note: The application will create tables automatically on first run.

8. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Create `.env` file** (optional, defaults to http://localhost:8000):
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Start the development server**:
   ```bash
   npm start
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000

## Usage Guide

### Creating a Workflow

1. **Open the application** in your browser
2. **Drag components** from the left panel onto the canvas:
   - User Query (entry point)
   - Knowledge Base (optional, for document search)
   - LLM Engine (required, for generating responses)
   - Output (required, for displaying results)

3. **Connect components** by dragging from output handles to input handles

4. **Configure components**:
   - Click on a component to open the configuration panel
   - Set up component-specific settings:
     - **Knowledge Base**: Upload documents, configure embedding provider
     - **LLM Engine**: Select provider (OpenAI/Gemini), model, temperature, etc.

5. **Save the workflow**:
   - Enter a workflow name
   - Click "Save Workflow"
   - Click "Validate" to check if the workflow is valid

### Using the Chat Interface

1. **Build and save a valid workflow**

2. **Click "Chat with Stack"** button

3. **Ask questions** in the chat interface

4. **The system will**:
   - Process your query through the workflow
   - Use knowledge base if connected
   - Generate response using LLM
   - Display the result

### Uploading Documents

1. **Add a Knowledge Base component** to your workflow

2. **Click on the component** to open configuration

3. **Click "Choose File"** and select a PDF or text document

4. **Wait for processing** (document will be extracted, embedded, and stored)

5. **Documents are now searchable** when the workflow executes

## Troubleshooting

### Backend Issues

- **Database connection errors**: Check PostgreSQL is running and credentials are correct
- **API key errors**: Verify API keys are set correctly in `.env`
- **Import errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)

### Frontend Issues

- **API connection errors**: Check backend is running on port 8000
- **Build errors**: Clear `node_modules` and reinstall (`rm -rf node_modules && npm install`)
- **CORS errors**: Verify CORS settings in `backend/app/core/config.py`

### Docker Issues

- **Port conflicts**: Change ports in `docker-compose.yml` if 3000 or 8000 are in use
- **Volume permissions**: On Linux, you may need to adjust permissions for mounted volumes
- **Build failures**: Check Docker logs: `docker-compose logs`

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
assignment/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── main.py       # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API services
│   │   └── App.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── .env.example
```

## Next Steps

- Review the [Architecture Documentation](ARCHITECTURE.md)
- Check the [README](README.md) for more details
- Explore the API documentation at `/docs`
- Customize components and add new features

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs in the console/terminal
3. Check API documentation for endpoint details
4. Verify all environment variables are set correctly

