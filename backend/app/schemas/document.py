"""
Document Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentUpload(BaseModel):
    """Schema for document upload"""
    knowledgebase_id: Optional[str] = None


class DocumentResponse(BaseModel):
    """Schema for document response"""
    id: int
    filename: str
    file_path: str
    file_size: int
    file_type: str
    knowledgebase_id: Optional[str]
    processed: str
    created_at: datetime
    updated_at: Optional[datetime]
    metadata_json: Optional[str]
    
    class Config:
        from_attributes = True

