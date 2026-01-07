"""
Execution Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class WorkflowExecute(BaseModel):
    """Schema for executing a workflow"""
    query: str = Field(..., description="User query to process")
    session_id: Optional[str] = Field(None, description="Chat session ID")
    workflow_id: int = Field(..., description="Workflow ID to execute")


class ExecutionResponse(BaseModel):
    """Schema for execution response"""
    success: bool
    response: str
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

