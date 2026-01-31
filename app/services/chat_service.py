"""
Chat Service for PetikSendiri Assistant
Handles chat sessions and message management
"""
import uuid
from typing import Optional, List, Tuple
from datetime import datetime

from sqlalchemy.orm import Session
from app.models.chat import ChatSession, ChatMessage, MessageRole
from app.services.rag_service import rag_service, RAGService


class ChatService:
    """Service for chat operations"""
    
    @staticmethod
    def create_session(db: Session, user_id: Optional[int] = None) -> ChatSession:
        """Create a new chat session with welcome message"""
        session_id = str(uuid.uuid4())
        
        chat_session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            title="New Chat"
        )
        db.add(chat_session)
        db.commit()
        db.refresh(chat_session)
        
        # Add welcome message
        welcome_message = ChatMessage(
            session_id=chat_session.id,
            role=MessageRole.ASSISTANT,
            content=RAGService.FIRST_MESSAGE
        )
        db.add(welcome_message)
        db.commit()
        
        return chat_session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[ChatSession]:
        """Get a chat session by session_id"""
        return db.query(ChatSession).filter(
            ChatSession.session_id == session_id
        ).first()
    
    @staticmethod
    def get_session_by_id(db: Session, id: int) -> Optional[ChatSession]:
        """Get a chat session by id"""
        return db.query(ChatSession).filter(ChatSession.id == id).first()
    
    @staticmethod
    def get_user_sessions(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[ChatSession]:
        """Get all chat sessions for a user"""
        return db.query(ChatSession).filter(
            ChatSession.user_id == user_id
        ).order_by(ChatSession.updated_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_session_messages(
        db: Session,
        session_id: str
    ) -> List[ChatMessage]:
        """Get all messages for a session"""
        session = ChatService.get_session(db, session_id)
        if not session:
            return []
        
        return db.query(ChatMessage).filter(
            ChatMessage.session_id == session.id
        ).order_by(ChatMessage.created_at.asc()).all()
    
    @staticmethod
    def get_chat_history(db: Session, session_id: str) -> List[Tuple[str, str]]:
        """Get chat history as list of (human, ai) tuples for RAG context"""
        messages = ChatService.get_session_messages(db, session_id)
        
        history = []
        human_msg = None
        
        for msg in messages:
            if msg.role == MessageRole.USER:
                human_msg = msg.content
            elif msg.role == MessageRole.ASSISTANT and human_msg is not None:
                history.append((human_msg, msg.content))
                human_msg = None
        
        return history
    
    @staticmethod
    def add_message(
        db: Session,
        session: ChatSession,
        role: MessageRole,
        content: str
    ) -> ChatMessage:
        """Add a message to a session"""
        message = ChatMessage(
            session_id=session.id,
            role=role,
            content=content
        )
        db.add(message)
        
        # Update session title if it's the first user message
        if role == MessageRole.USER:
            user_messages = db.query(ChatMessage).filter(
                ChatMessage.session_id == session.id,
                ChatMessage.role == MessageRole.USER
            ).count()
            
            if user_messages == 0:  # This will be the first
                # Generate title from first message
                title = content[:50] + "..." if len(content) > 50 else content
                session.title = title
        
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
        
        return message
    
    @staticmethod
    def process_message(
        db: Session,
        session_id: Optional[str],
        user_message: str,
        user_id: Optional[int] = None
    ) -> Tuple[ChatSession, ChatMessage, bool]:
        """
        Process a user message and generate response
        Returns: (session, assistant_message, is_new_session)
        """
        is_new_session = False
        
        # Get or create session
        if session_id:
            session = ChatService.get_session(db, session_id)
            if not session:
                # Session not found, create new one
                session = ChatService.create_session(db, user_id)
                is_new_session = True
        else:
            session = ChatService.create_session(db, user_id)
            is_new_session = True
        
        # Add user message
        ChatService.add_message(db, session, MessageRole.USER, user_message)
        
        # Get chat history for context
        chat_history = ChatService.get_chat_history(db, session.session_id)
        
        # Generate response using RAG
        response_content = rag_service.generate_response(
            user_message=user_message,
            chat_history=chat_history
        )
        
        # Add assistant message
        assistant_message = ChatService.add_message(
            db, session, MessageRole.ASSISTANT, response_content
        )
        
        return session, assistant_message, is_new_session
    
    @staticmethod
    def delete_session(db: Session, session_id: str) -> bool:
        """Delete a chat session and all its messages"""
        session = ChatService.get_session(db, session_id)
        if not session:
            return False
        
        db.delete(session)
        db.commit()
        return True
    
    @staticmethod
    def update_session_title(
        db: Session,
        session_id: str,
        title: str
    ) -> Optional[ChatSession]:
        """Update the title of a chat session"""
        session = ChatService.get_session(db, session_id)
        if not session:
            return None
        
        session.title = title
        db.commit()
        db.refresh(session)
        return session
