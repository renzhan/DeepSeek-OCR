"""Configuration management for the FastAPI OCR service."""

import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Service configuration
    host: str = Field(default="0.0.0.0", description="Host to bind the service")
    port: int = Field(default=8000, description="Port to bind the service")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # OCR configuration
    model_path: str = Field(default="deepseek-ai/DeepSeek-OCR", description="Path to DeepSeek OCR model")
    max_file_size: int = Field(default=50 * 1024 * 1024, description="Maximum file size in bytes (50MB)")
    
    # Storage configuration
    temp_dir: str = Field(default="/tmp/ocr_temp", description="Temporary file storage directory")
    cleanup_interval: int = Field(default=3600, description="Cleanup interval in seconds")
    
    # Processing configuration
    default_prompt: str = Field(
        default="<image>\n<|grounding|>Convert the document to markdown.",
        description="Default prompt for OCR processing"
    )
    base_size: int = Field(default=1024, description="Base image size for processing")
    image_size: int = Field(default=640, description="Image size for processing")
    crop_mode: bool = Field(default=True, description="Enable crop mode by default")
    min_crops: int = Field(default=2, description="Minimum number of crops")
    max_crops: int = Field(default=6, description="Maximum number of crops")
    max_concurrency: int = Field(default=100, description="Maximum concurrency for processing")
    num_workers: int = Field(default=64, description="Number of worker threads")
    skip_repeat: bool = Field(default=True, description="Skip repeated content")
    
    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    class Config:
        env_file = ".env"
        env_prefix = "OCR_"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def create_temp_dir() -> None:
    """Create temporary directory if it doesn't exist."""
    os.makedirs(settings.temp_dir, exist_ok=True)


def validate_model_path() -> bool:
    """Validate that the model path exists or is accessible."""
    # For now, we'll assume the model path is valid
    # In a real implementation, you might want to check if it's a valid HuggingFace model
    return bool(settings.model_path)