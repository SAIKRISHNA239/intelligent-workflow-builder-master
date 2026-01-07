"""
Workflow database models
"""
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Workflow(Base):
    """Workflow model"""
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    components = relationship("WorkflowComponent", back_populates="workflow", cascade="all, delete-orphan")
    connections = relationship("ComponentConnection", back_populates="workflow", cascade="all, delete-orphan")


class WorkflowComponent(Base):
    """Workflow component model"""
    __tablename__ = "workflow_components"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    component_type = Column(String(50), nullable=False)  # user_query, knowledgebase, llm_engine, output
    node_id = Column(String(100), nullable=False)  # React Flow node ID
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    config = Column(JSON, nullable=True)  # Component-specific configuration
    
    # Relationships
    workflow = relationship("Workflow", back_populates="components")
    source_connections = relationship("ComponentConnection", foreign_keys="ComponentConnection.source_component_id", back_populates="source_component")
    target_connections = relationship("ComponentConnection", foreign_keys="ComponentConnection.target_component_id", back_populates="target_component")


class ComponentConnection(Base):
    """Component connection model"""
    __tablename__ = "component_connections"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    source_component_id = Column(Integer, ForeignKey("workflow_components.id"), nullable=False)
    target_component_id = Column(Integer, ForeignKey("workflow_components.id"), nullable=False)
    source_handle = Column(String(50), nullable=True)
    target_handle = Column(String(50), nullable=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="connections")
    source_component = relationship("WorkflowComponent", foreign_keys=[source_component_id], back_populates="source_connections")
    target_component = relationship("WorkflowComponent", foreign_keys=[target_component_id], back_populates="target_connections")

