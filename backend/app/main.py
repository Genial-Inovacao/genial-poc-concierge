from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .database import engine, Base
from .api import auth, users, suggestions, transactions, analytics, interactions


# Create all tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: Welcome message
    """
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs"
    }


# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(suggestions.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(interactions.router, prefix="/api")