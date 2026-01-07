"""
Workflow Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ComponentCreate(BaseModel):
    """Schema for creating a workflow component"""
    component_type: str = Field(..., description="Type of component: user_query, knowledgebase, llm_engine, output")
    node_id: str = Field(..., description="React Flow node ID")
    position_x: int = Field(..., description="X position on canvas")
    position_y: int = Field(..., description="Y position on canvas")
    config: Optional[Dict[str, Any]] = Field(None, description="Component-specific configuration")


class ComponentResponse(BaseModel):
    """Schema for component response"""
    id: int
    workflow_id: int
    component_type: str
    node_id: str
    position_x: int
    position_y: int
    config: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True


class ConnectionCreate(BaseModel):
    """Schema for creating a component connection"""
    source_component_id: str = Field(..., description="Source component node ID (from React Flow)")
    target_component_id: str = Field(..., description="Target component node ID (from React Flow)")
    source_handle: Optional[str] = Field(None, description="Source handle ID")
    target_handle: Optional[str] = Field(None, description="Target handle ID")


class ConnectionResponse(BaseModel):
    """Schema for connection response"""
    id: int
    workflow_id: int
    source_component_id: int
    target_component_id: int
    source_handle: Optional[str]
    target_handle: Optional[str]
    
    class Config:
        from_attributes = True


class WorkflowCreate(BaseModel):
    """Schema for creating a workflow"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    components: List[ComponentCreate] = Field(default_factory=list)
    connections: List[ConnectionCreate] = Field(default_factory=list)


class WorkflowUpdate(BaseModel):
    """Schema for updating a workflow"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    components: Optional[List[ComponentCreate]] = None
    connections: Optional[List[ConnectionCreate]] = None


class WorkflowResponse(BaseModel):
    """Schema for workflow response"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    components: List[ComponentResponse] = []
    connections: List[ConnectionResponse] = []
    
    class Config:
        from_attributes = True

