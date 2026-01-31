from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## PetikSendiri API
    
    Backend API untuk aplikasi PetikSendiri.
    
    ### Features:
    * **User Management** - Create, read, update, and delete users
    * **Authentication** - JWT-based authentication
    * **PetikSendiri Assistant** - AI Chatbot dengan RAG untuk urban farming
    
    ### Authentication:
    Use the `/api/v1/auth/login` endpoint to get an access token,
    then include it in the Authorization header as `Bearer <token>`.
    
    ### PetikSendiri Assistant:
    AI Chatbot yang dapat menjawab pertanyaan seputar urban farming dan tanaman.
    Menggunakan RAG (Retrieval-Augmented Generation) dengan knowledge base dari dokumen PDF/DOCX/TXT.
    """,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - Health check.
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
