from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Chat Message Schemas
class ChatMessageBase(BaseModel):
    role: MessageRole
    content: str


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(ChatMessageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Chat Session Schemas
class ChatSessionBase(BaseModel):
    title: Optional[str] = "New Chat"


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionResponse(ChatSessionBase):
    id: int
    session_id: str
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ChatSessionWithMessages(ChatSessionResponse):
    messages: List[ChatMessageResponse] = []


# Chat Request/Response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    message: ChatMessageResponse
    is_new_session: bool = False


# Document Processing Schemas
class DocumentProcessRequest(BaseModel):
    force_reprocess: bool = False


class ProcessedDocumentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    file_type: str
    chunk_count: int
    status: str
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentProcessingStatus(BaseModel):
    total_files: int
    processed: int
    failed: int
    pending: int
    documents: List[ProcessedDocumentResponse]


class KnowledgeBaseStats(BaseModel):
    total_documents: int
    total_chunks: int
    vector_store_exists: bool
    last_updated: Optional[datetime] = None
