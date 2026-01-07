"""
Chat database models
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system
    message = Column(Text, nullable=False)
    meta = Column("metadata", JSON, nullable=True)  # Store execution metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

