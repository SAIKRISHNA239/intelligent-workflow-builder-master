"""
Chat API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.chat import ChatMessage
from app.models.workflow import Workflow
from app.schemas.chat import ChatMessageCreate, ChatMessageResponse
from app.services.workflow_executor import WorkflowExecutor

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(message_data: ChatMessageCreate, db: Session = Depends(get_db)):
    """Send a chat message through a workflow"""
    # Validate message
    if not message_data.message or not message_data.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    # Save user message
    user_message = ChatMessage(
        workflow_id=message_data.workflow_id,
        session_id=message_data.session_id,
        role="user",
        message=message_data.message.strip()
    )
    db.add(user_message)
    db.flush()
    
    # Get workflow with components and connections
    from sqlalchemy.orm import joinedload
    workflow = db.query(Workflow)\
        .options(joinedload(Workflow.components), joinedload(Workflow.connections))\
        .filter(Workflow.id == message_data.workflow_id)\
        .first()
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    # Ensure components and connections are loaded
    _ = workflow.components
    _ = workflow.connections
    
    # Execute workflow
    executor = WorkflowExecutor()
    result = executor.execute_workflow(workflow, message_data.message.strip(), db)
    
    # Save assistant response
    assistant_message = ChatMessage(
        workflow_id=message_data.workflow_id,
        session_id=message_data.session_id,
        role="assistant",
        message=result.get("response", "") if result.get("success") else f"Error: {result.get('error', 'Unknown error')}",
        meta=result.get("metadata")
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    
    return assistant_message


@router.get("/sessions/{session_id}", response_model=List[ChatMessageResponse])
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    """Get chat history for a session"""
    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.asc()).all()
    
    return messages


@router.get("/workflows/{workflow_id}/sessions", response_model=List[str])
def list_sessions(workflow_id: int, db: Session = Depends(get_db)):
    """List all chat sessions for a workflow"""
    sessions = db.query(ChatMessage.session_id).filter(
        ChatMessage.workflow_id == workflow_id
    ).distinct().all()
    
    return [session[0] for session in sessions]

