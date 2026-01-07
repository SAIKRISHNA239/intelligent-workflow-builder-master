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
    workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    executor = WorkflowExecutor()
    result = executor.execute_workflow(workflow, execution_data.query, db)
    
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

