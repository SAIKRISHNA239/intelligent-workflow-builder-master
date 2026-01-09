"""
Workflow execution API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.workflow import Workflow
from app.schemas.execution import WorkflowExecute, ExecutionResponse
from app.services.workflow_executor import WorkflowExecutor

router = APIRouter(prefix="/api/workflows", tags=["execution"])


@router.post("/{workflow_id}/execute", response_model=ExecutionResponse)
def execute_workflow(
    workflow_id: int,
    execution_data: WorkflowExecute,
    db: Session = Depends(get_db)
):
    """Execute a workflow with a query"""
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
    
    # Ensure components and connections are loaded
    _ = workflow.components
    _ = workflow.connections
    
    # Validate query
    if not execution_data.query or not execution_data.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
    
    executor = WorkflowExecutor()
    result = executor.execute_workflow(workflow, execution_data.query.strip(), db)
    
    if not result["success"]:
        return ExecutionResponse(
            success=False,
            response="",
            error=result["error"]
        )
    
    return ExecutionResponse(
        success=True,
        response=result["response"],
        metadata=result.get("metadata")
    )

