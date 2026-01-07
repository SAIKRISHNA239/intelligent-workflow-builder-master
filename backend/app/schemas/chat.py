"""
Chat Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    workflow_id: int
    session_id: str
    message: str
    role: str = "user"


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    workflow_id: Optional[int]
    session_id: str
    role: str
    message: str
    metadata: Optional[Dict[str, Any]] = Field(default=None, validation_alias="meta")
    created_at: datetime


