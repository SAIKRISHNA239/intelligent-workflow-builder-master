"""
Document API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime
from app.core.database import get_db
from app.core.config import settings
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.text_extractor import TextExtractor
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStoreService

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    knowledgebase_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    # Validate file size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Create document record
    document = Document(
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file.content_type or "application/octet-stream",
        knowledgebase_id=knowledgebase_id,
        processed="pending"
    )
    db.add(document)
    db.flush()
    
    # Process document asynchronously (in production, use background tasks)
    try:
        # Extract text
        text_extractor = TextExtractor()
        text_content = text_extractor.extract_text(file_path, document.file_type)
        
        # Split text into chunks (simple chunking by paragraphs)
        chunks = [chunk.strip() for chunk in text_content.split("\n\n") if chunk.strip()]
        
        if chunks:
            # Generate embeddings
            embedding_service = EmbeddingService()
            embedding_provider = "openai"  # Can be configured
            embeddings = embedding_service.generate_embeddings(
                chunks,
                provider=embedding_provider
            )
            
            # Store in vector database
            vector_store = VectorStoreService()
            collection_name = knowledgebase_id or "default"
            metadatas = [
                {
                    "document_id": document.id,
                    "filename": file.filename,
                    "chunk_index": i
                }
                for i in range(len(chunks))
            ]
            
            vector_store.add_documents(
                collection_name=collection_name,
                knowledgebase_id=knowledgebase_id or "default",
                texts=chunks,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            document.processed = "completed"
            document.metadata_json = f'{{"chunks": {len(chunks)}, "embedding_provider": "{embedding_provider}"}}'
        else:
            document.processed = "failed"
            document.metadata_json = '{"error": "No text content extracted"}'
    
    except Exception as e:
        document.processed = "failed"
        document.metadata_json = f'{{"error": "{str(e)}"}}'
    
    db.commit()
    db.refresh(document)
    
    return document


@router.get("", response_model=List[DocumentResponse])
def list_documents(
    knowledgebase_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all documents"""
    query = db.query(Document)
    
    if knowledgebase_id:
        query = query.filter(Document.knowledgebase_id == knowledgebase_id)
    
    documents = query.offset(skip).limit(limit).all()
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get document by ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete document"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file if exists
    if os.path.exists(document.file_path):
        try:
            os.remove(document.file_path)
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
    
    db.delete(document)
    db.commit()
    
    return None

