"""
Workflow API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.workflow import Workflow, WorkflowComponent, ComponentConnection
from app.schemas.workflow import (
    WorkflowCreate, WorkflowUpdate, WorkflowResponse,
    ComponentCreate, ComponentResponse,
    ConnectionCreate, ConnectionResponse
)
from app.services.workflow_executor import WorkflowExecutor

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(workflow_data: WorkflowCreate, db: Session = Depends(get_db)):
    """Create a new workflow"""
    # Create workflow
    workflow = Workflow(
        name=workflow_data.name,
        description=workflow_data.description
    )
    db.add(workflow)
    db.flush()
    
    # Create components
    component_map = {}
    for comp_data in workflow_data.components:
        component = WorkflowComponent(
            workflow_id=workflow.id,
            component_type=comp_data.component_type,
            node_id=comp_data.node_id,
            position_x=comp_data.position_x,
            position_y=comp_data.position_y,
            config=comp_data.config
        )
        db.add(component)
        db.flush()
        component_map[comp_data.node_id] = component
    
    # Create connections - map node IDs to component IDs
    node_to_component = {comp.node_id: comp.id for comp in component_map.values()}
    
    for conn_data in workflow_data.connections:
        # Find components by node_id (from React Flow)
        source_comp = component_map.get(conn_data.source_component_id)
        target_comp = component_map.get(conn_data.target_component_id)
        
        if not source_comp or not target_comp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid node IDs in connection: {conn_data.source_component_id} -> {conn_data.target_component_id}"
            )
        
        connection = ComponentConnection(
            workflow_id=workflow.id,
            source_component_id=source_comp.id,
            target_component_id=target_comp.id,
            source_handle=conn_data.source_handle,
            target_handle=conn_data.target_handle
        )
        db.add(connection)
    
    db.commit()
    
    # Reload workflow with relationships
    from sqlalchemy.orm import joinedload
    workflow = db.query(Workflow)\
        .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
        .filter(Workflow.id == workflow.id)\
        .first()
    
    return workflow


@router.get("", response_model=List[WorkflowResponse])
def list_workflows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all workflows"""
    from sqlalchemy.orm import joinedload
    
    workflows = db.query(Workflow)\
        .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
        .offset(skip)\
        .limit(limit)\
        .all()
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Get workflow by ID"""
    from sqlalchemy.orm import joinedload
    
    # Eagerly load components and connections
    workflow = db.query(Workflow)\
        .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
        .filter(Workflow.id == workflow_id)\
        .first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    return workflow


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    """Update workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    try:
        if workflow_data.name:
            workflow.name = workflow_data.name
        if workflow_data.description is not None:
            workflow.description = workflow_data.description
        
        # Update components and connections if provided
        if workflow_data.components is not None:
            # Delete existing components and connections
            db.query(ComponentConnection).filter(ComponentConnection.workflow_id == workflow_id).delete()
            db.query(WorkflowComponent).filter(WorkflowComponent.workflow_id == workflow_id).delete()
            db.flush()
            
            # Create new components
            component_map = {}
            if not workflow_data.components:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Workflow must contain at least one component"
                )
            
            for comp_data in workflow_data.components:
                component = WorkflowComponent(
                    workflow_id=workflow.id,
                    component_type=comp_data.component_type,
                    node_id=comp_data.node_id,
                    position_x=comp_data.position_x,
                    position_y=comp_data.position_y,
                    config=comp_data.config or {}
                )
                db.add(component)
                db.flush()
                component_map[comp_data.node_id] = component
            
            # Create new connections - map node IDs to component IDs
            if workflow_data.connections:
                invalid_connections = []
                for conn_data in workflow_data.connections:
                    # Find components by node_id (from React Flow)
                    source_comp = component_map.get(conn_data.source_component_id)
                    target_comp = component_map.get(conn_data.target_component_id)
                    
                    if not source_comp or not target_comp:
                        invalid_connections.append(
                            f"Connection from {conn_data.source_component_id} to {conn_data.target_component_id} references non-existent components"
                        )
                        continue
                    
                    connection = ComponentConnection(
                        workflow_id=workflow.id,
                        source_component_id=source_comp.id,
                        target_component_id=target_comp.id,
                        source_handle=conn_data.source_handle,
                        target_handle=conn_data.target_handle
                    )
                    db.add(connection)
                
                if invalid_connections:
                    # Log warning but don't fail - just skip invalid connections
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Invalid connections skipped: {', '.join(invalid_connections)}")
        
        db.commit()
        
        # Refresh and reload with relationships
        db.refresh(workflow)
        # Explicitly reload components and connections
        from sqlalchemy.orm import joinedload
        workflow = db.query(Workflow)\
            .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
            .filter(Workflow.id == workflow.id)\
            .first()
        
        return workflow
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating workflow: {str(e)}"
        )


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Delete workflow"""
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    db.delete(workflow)
    db.commit()
    
    return None


@router.post("/{workflow_id}/validate", status_code=status.HTTP_200_OK)
def validate_workflow(workflow_id: int, db: Session = Depends(get_db)):
    """Validate workflow structure"""
    from sqlalchemy.orm import joinedload
    
    # Eagerly load components and connections to ensure they're available
    workflow = db.query(Workflow)\
        .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
        .filter(Workflow.id == workflow_id)\
        .first()
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    # Ensure components and connections are loaded
    _ = workflow.components  # Access to trigger lazy load if needed
    _ = workflow.connections  # Access to trigger lazy load if needed
    
    executor = WorkflowExecutor()
    is_valid, error = executor.validate_workflow(workflow)
    
    return {
        "valid": is_valid,
        "error": error
    }

