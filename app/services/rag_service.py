"""
RAG (Retrieval-Augmented Generation) Service for PetikSendiri Assistant
Handles document processing, vector store management, and knowledge retrieval
"""
import os
import logging
from typing import List, Optional, Tuple
from datetime import datetime
from pathlib import Path

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.chat import ProcessedDocument

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG operations including document processing and retrieval"""
    
    FIRST_MESSAGE = (
        "Hai, Sobat Petik Sendiri 👋. Sekarang Anda terhubung dengan PetikSendiri Asisten, "
        "asisten pintar yang bantu temukan info seputar urban farming. Apa yang bisa saya bantu?"
    )
    
    SYSTEM_PROMPT = """Kamu adalah PetikSendiri Assistant, asisten AI yang ahli dalam bidang urban farming dan tanaman.

ATURAN PENTING:
1. KECUALI untuk sapaan dan pertanyaan identitas, kamu HANYA boleh menjawab pertanyaan yang berkaitan dengan:
   - Urban farming (pertanian perkotaan)
   - Tanaman (cara menanam, merawat, panen, dll)
   - Hidroponik dan aquaponik
   - Berkebun di rumah/apartemen
   - Tips pertanian skala kecil
   - Jenis-jenis tanaman dan karakteristiknya
   - Hama dan penyakit tanaman
   - Pupuk dan nutrisi tanaman

2. KHUSUS untuk sapaan ("Hai", "Halo", "Halo kak", dll) dan pertanyaan identitas ("Kamu siapa?", "Siapa kamu?", "Apa itu PetikSendiri?", dll):
   - Jawab dengan ramah dan perkenalkan dirimu sebagai PetikSendiri Assistant
   - Jelaskan bahwa kamu adalah asisten AI yang siap membantu pertanyaan seputar urban farming dan tanaman
   - Ajak user untuk bertanya tentang urban farming

3. Jika pertanyaan TIDAK berkaitan dengan topik di atas DAN bukan sapaan/identitas, jawab dengan sopan:
   "Maaf, saya hanya bisa membantu menjawab pertanyaan seputar urban farming dan tanaman. Silakan ajukan pertanyaan yang berkaitan dengan topik tersebut ya! 🌱"

4. Gunakan bahasa Indonesia yang ramah dan mudah dipahami.

5. Jika ada konteks dari knowledge base, gunakan informasi tersebut untuk menjawab.

6. Selalu berikan jawaban yang informatif dan praktis.

7. BATASAN PANJANG JAWABAN: Jawab dengan SINGKAT dan PADAT, maksimal 50-80 kata. Kecuali jika user meminta penjelasan detail.

KONTEKS DARI KNOWLEDGE BASE:
{context}

Jika konteks kosong atau tidak relevan, jawab berdasarkan pengetahuanmu tentang urban farming."""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0.7
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store: Optional[FAISS] = None
        self._load_vector_store()
    
    def _get_knowledge_base_path(self) -> Path:
        """Get the knowledge base directory path"""
        return Path(settings.KNOWLEDGE_BASE_PATH)
    
    def _get_vector_store_path(self) -> Path:
        """Get the vector store directory path"""
        return Path(settings.VECTOR_STORE_PATH)
    
    def _load_vector_store(self) -> None:
        """Load existing vector store if available"""
        vector_store_path = self._get_vector_store_path()
        index_path = vector_store_path / "index.faiss"
        
        if index_path.exists():
            try:
                self.vector_store = FAISS.load_local(
                    str(vector_store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("Vector store loaded successfully")
            except Exception as e:
                logger.error(f"Error loading vector store: {e}")
                self.vector_store = None
        else:
            logger.info("No existing vector store found")
    
    def _load_document(self, file_path: str) -> List[Document]:
        """Load a document based on its file type"""
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        try:
            if extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif extension == ".docx":
                loader = Docx2txtLoader(str(file_path))
            elif extension == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
            else:
                logger.warning(f"Unsupported file type: {extension}")
                return []
            
            documents = loader.load()
            # Add metadata
            for doc in documents:
                doc.metadata["source"] = str(file_path)
                doc.metadata["filename"] = file_path.name
            
            return documents
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {e}")
            return []
    
    def get_all_files(self) -> List[Tuple[str, str]]:
        """Get all supported files from knowledge base directory"""
        knowledge_base_path = self._get_knowledge_base_path()
        
        if not knowledge_base_path.exists():
            knowledge_base_path.mkdir(parents=True, exist_ok=True)
            return []
        
        supported_extensions = {".pdf", ".docx", ".txt"}
        files = []
        
        for file_path in knowledge_base_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                files.append((str(file_path), file_path.suffix.lower()[1:]))
        
        return files
    
    def process_documents(self, db: Session, force_reprocess: bool = False) -> dict:
        """Process all documents in knowledge base and create/update vector store"""
        files = self.get_all_files()
        
        if not files:
            return {
                "success": False,
                "message": "No documents found in knowledge base",
                "processed": 0,
                "failed": 0
            }
        
        all_documents = []
        processed_count = 0
        failed_count = 0
        
        for file_path, file_type in files:
            # Check if already processed
            existing = db.query(ProcessedDocument).filter(
                ProcessedDocument.file_path == file_path
            ).first()
            
            if existing and not force_reprocess:
                if existing.status == "completed":
                    logger.info(f"Skipping already processed: {file_path}")
                    continue
            
            # Create or update record
            if not existing:
                doc_record = ProcessedDocument(
                    filename=Path(file_path).name,
                    file_path=file_path,
                    file_type=file_type,
                    status="processing"
                )
                db.add(doc_record)
            else:
                doc_record = existing
                doc_record.status = "processing"
                doc_record.error_message = None
            
            db.commit()
            
            try:
                # Load and split document
                documents = self._load_document(file_path)
                if documents:
                    chunks = self.text_splitter.split_documents(documents)
                    all_documents.extend(chunks)
                    
                    doc_record.chunk_count = len(chunks)
                    doc_record.status = "completed"
                    doc_record.processed_at = datetime.utcnow()
                    processed_count += 1
                else:
                    doc_record.status = "failed"
                    doc_record.error_message = "No content extracted from document"
                    failed_count += 1
            except Exception as e:
                doc_record.status = "failed"
                doc_record.error_message = str(e)
                failed_count += 1
                logger.error(f"Error processing {file_path}: {e}")
            
            db.commit()
        
        # Create or update vector store
        if all_documents:
            try:
                vector_store_path = self._get_vector_store_path()
                vector_store_path.mkdir(parents=True, exist_ok=True)
                
                if self.vector_store is None or force_reprocess:
                    self.vector_store = FAISS.from_documents(
                        all_documents,
                        self.embeddings
                    )
                else:
                    self.vector_store.add_documents(all_documents)
                
                self.vector_store.save_local(str(vector_store_path))
                logger.info(f"Vector store saved with {len(all_documents)} chunks")
            except Exception as e:
                logger.error(f"Error creating vector store: {e}")
                return {
                    "success": False,
                    "message": f"Error creating vector store: {e}",
                    "processed": processed_count,
                    "failed": failed_count
                }
        
        return {
            "success": True,
            "message": f"Processed {processed_count} documents, {failed_count} failed",
            "processed": processed_count,
            "failed": failed_count,
            "total_chunks": len(all_documents)
        }
    
    def retrieve_context(self, query: str, k: int = 4) -> str:
        """Retrieve relevant context from vector store"""
        if self.vector_store is None:
            return ""
        
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            if not docs:
                return ""
            
            context_parts = []
            for i, doc in enumerate(docs, 1):
                source = doc.metadata.get("filename", "Unknown")
                context_parts.append(f"[Sumber: {source}]\n{doc.page_content}")
            
            return "\n\n---\n\n".join(context_parts)
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return ""
    
    def generate_response(
        self,
        user_message: str,
        chat_history: List[Tuple[str, str]] = None
    ) -> str:
        """Generate a response using RAG"""
        # Retrieve context
        context = self.retrieve_context(user_message)
        
        # Build messages
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT.format(context=context if context else "Tidak ada konteks tersedia."))
        ]
        
        # Add chat history
        if chat_history:
            for human_msg, ai_msg in chat_history[-5:]:  # Last 5 exchanges
                messages.append(HumanMessage(content=human_msg))
                messages.append(AIMessage(content=ai_msg))
        
        # Add current message
        messages.append(HumanMessage(content=user_message))
        
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi."
    
    def get_knowledge_base_stats(self, db: Session) -> dict:
        """Get statistics about the knowledge base"""
        documents = db.query(ProcessedDocument).all()
        
        total_documents = len(documents)
        total_chunks = sum(doc.chunk_count for doc in documents if doc.status == "completed")
        
        vector_store_exists = (self._get_vector_store_path() / "index.faiss").exists()
        
        last_processed = db.query(ProcessedDocument).filter(
            ProcessedDocument.status == "completed"
        ).order_by(ProcessedDocument.processed_at.desc()).first()
        
        return {
            "total_documents": total_documents,
            "total_chunks": total_chunks,
            "vector_store_exists": vector_store_exists,
            "last_updated": last_processed.processed_at if last_processed else None
        }


# Singleton instance
rag_service = RAGService()
