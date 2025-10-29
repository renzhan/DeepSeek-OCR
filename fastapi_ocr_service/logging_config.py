"""Logging configuration for the FastAPI OCR service."""

import logging
import sys
from typing import Dict, Any

from .config import Settings


def setup_logging(settings: Settings) -> None:
    """Setup logging configuration."""
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Configure specific loggers
    loggers_config = {
        "fastapi_ocr_service": settings.log_level.upper(),
        "uvicorn": "INFO",
        "uvicorn.error": "INFO", 
        "uvicorn.access": "INFO" if settings.debug else "WARNING"
    }
    
    for logger_name, level in loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, level))


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(f"fastapi_ocr_service.{name}")


class LoggerMixin:
    """Mixin class to add logging capability to other classes."""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        return get_logger(self.__class__.__name__)


def log_request_info(
    method: str,
    path: str,
    file_type: str = None,
    file_size: int = None,
    processing_time: float = None
) -> None:
    """Log request information."""
    logger = get_logger("request")
    
    info_parts = [f"{method} {path}"]
    
    if file_type:
        info_parts.append(f"file_type={file_type}")
    
    if file_size:
        info_parts.append(f"file_size={file_size}")
    
    if processing_time:
        info_parts.append(f"processing_time={processing_time:.2f}s")
    
    logger.info(" | ".join(info_parts))


def log_error_info(
    error_code: str,
    error_message: str,
    details: Dict[str, Any] = None
) -> None:
    """Log error information."""
    logger = get_logger("error")
    
    error_info = f"Error {error_code}: {error_message}"
    
    if details:
        error_info += f" | Details: {details}"
    
    logger.error(error_info)