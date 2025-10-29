"""Main FastAPI application for OCR service."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import __version__, __description__
from .app_state import app_state
from .config import get_settings, create_temp_dir
from .logging_config import setup_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger = get_logger("main")
    settings = get_settings()
    
    # Startup
    logger.info("Starting FastAPI OCR Service...")
    
    # Initialize app state
    app_state.initialize(settings)
    
    # Create temporary directory
    create_temp_dir()
    logger.info(f"Created temporary directory: {settings.temp_dir}")
    
    # TODO: Initialize OCR engine (will be implemented in task 2.1)
    logger.info("OCR engine initialization will be implemented in task 2.1")
    
    logger.info(f"FastAPI OCR Service v{__version__} started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI OCR Service...")
    
    # TODO: Cleanup resources
    logger.info("Cleanup completed")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()
    
    # Setup logging
    setup_logging(settings)
    
    # Create FastAPI app
    app = FastAPI(
        title="FastAPI OCR Service",
        description=__description__,
        version=__version__,
        lifespan=lifespan,
        debug=settings.debug
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # TODO: Add routes (will be implemented in task 4.1)
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    
    uvicorn.run(
        "fastapi_ocr_service.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )