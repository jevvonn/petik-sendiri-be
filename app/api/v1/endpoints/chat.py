"""
Chat API Endpoints for PetikSendiri Assistant
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatSessionWithMessages,
    ChatMessageResponse,
    DocumentProcessRequest,
    DocumentProcessingStatus,
    ProcessedDocumentResponse,
    KnowledgeBaseStats
)
from app.services.chat_service import ChatService
from app.services.rag_service import rag_service, RAGService
from app.api.deps import get_current_active_user, get_current_user, get_optional_user
from app.models.user import User
from app.models.chat import ProcessedDocument

router = APIRouter()


# ==================== Chat Endpoints ====================

@router.post("/send", response_model=ChatResponse, summary="Send Chat Message")
def send_message(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Send a message to PetikSendiri Assistant and get a response.
    
    - **message**: The user's message/question
    - **session_id**: Optional session ID for continuing a conversation
    
    If no session_id is provided, a new session will be created.
    The assistant only answers questions about urban farming and plants.
    """
    user_id = current_user.id if current_user else None
    
    session, assistant_message, is_new_session = ChatService.process_message(
        db=db,
        session_id=request.session_id,
        user_message=request.message,
        user_id=user_id
    )
    
    return ChatResponse(
        session_id=session.session_id,
        message=ChatMessageResponse(
            id=assistant_message.id,
            role=assistant_message.role,
            content=assistant_message.content,
            created_at=assistant_message.created_at
        ),
        is_new_session=is_new_session
    )


@router.post("/sessions", response_model=ChatSessionWithMessages, summary="Create New Chat Session")
def create_session(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Create a new chat session.
    
    Returns the session with the welcome message from PetikSendiri Assistant.
    """
    user_id = current_user.id if current_user else None
    session = ChatService.create_session(db, user_id)
    
    messages = ChatService.get_session_messages(db, session.session_id)
    
    return ChatSessionWithMessages(
        id=session.id,
        session_id=session.session_id,
        user_id=session.user_id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=[
            ChatMessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            ) for msg in messages
        ]
    )


@router.get("/sessions", response_model=List[ChatSessionResponse], summary="Get User's Chat Sessions")
def get_sessions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all chat sessions for the authenticated user.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    sessions = ChatService.get_user_sessions(
        db, current_user.id, skip=skip, limit=limit
    )
    
    return [
        ChatSessionResponse(
            id=session.id,
            session_id=session.session_id,
            user_id=session.user_id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at
        ) for session in sessions
    ]


@router.get("/sessions/{session_id}", response_model=ChatSessionWithMessages, summary="Get Chat Session with Messages")
def get_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get a specific chat session with all its messages.
    
    - **session_id**: The unique session ID
    """
    session = ChatService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    messages = ChatService.get_session_messages(db, session_id)
    
    return ChatSessionWithMessages(
        id=session.id,
        session_id=session.session_id,
        user_id=session.user_id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=[
            ChatMessageResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            ) for msg in messages
        ]
    )


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Chat Session")
def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a chat session and all its messages.
    
    - **session_id**: The unique session ID to delete
    """
    session = ChatService.get_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # Check ownership
    if session.user_id and session.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this session"
        )
    
    ChatService.delete_session(db, session_id)
    return None


# ==================== Knowledge Base Endpoints ====================

@router.post("/knowledge-base/process", response_model=dict, summary="Process Knowledge Base Documents")
def process_knowledge_base(
    request: DocumentProcessRequest = DocumentProcessRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Process all PDF/DOCX/TXT documents in the knowledge base folder
    and create/update the vector store.
    
    - **force_reprocess**: If True, reprocess all documents even if already processed
    
    Note: Only superusers can trigger document processing.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can process knowledge base"
        )
    
    result = rag_service.process_documents(db, request.force_reprocess)
    return result


@router.get("/knowledge-base/stats", response_model=KnowledgeBaseStats, summary="Get Knowledge Base Statistics")
def get_knowledge_base_stats(
    db: Session = Depends(get_db)
):
    """
    Get statistics about the knowledge base including:
    - Total documents processed
    - Total text chunks
    - Vector store status
    - Last update time
    """
    stats = rag_service.get_knowledge_base_stats(db)
    return KnowledgeBaseStats(**stats)


@router.get("/knowledge-base/documents", response_model=List[ProcessedDocumentResponse], summary="List Processed Documents")
def list_processed_documents(
    db: Session = Depends(get_db)
):
    """
    List all documents that have been processed for the knowledge base.
    """
    documents = db.query(ProcessedDocument).order_by(
        ProcessedDocument.created_at.desc()
    ).all()
    
    return [
        ProcessedDocumentResponse(
            id=doc.id,
            filename=doc.filename,
            file_path=doc.file_path,
            file_type=doc.file_type,
            chunk_count=doc.chunk_count,
            status=doc.status,
            error_message=doc.error_message,
            processed_at=doc.processed_at,
            created_at=doc.created_at
        ) for doc in documents
    ]


@router.get("/knowledge-base/files", response_model=List[dict], summary="List Available Files")
def list_available_files():
    """
    List all files available in the knowledge base folder that can be processed.
    """
    files = rag_service.get_all_files()
    return [
        {"file_path": file_path, "file_type": file_type}
        for file_path, file_type in files
    ]


@router.get("/first-message", response_model=dict, summary="Get First Message")
def get_first_message():
    """
    Get the welcome message for new chat sessions.
    """
    return {
        "message": RAGService.FIRST_MESSAGE
    }
