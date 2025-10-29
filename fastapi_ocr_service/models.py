"""Data models for the FastAPI OCR service."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FileType(str, Enum):
    """Supported file types."""
    IMAGE = "image"
    PDF = "pdf"


class OCRConfig(BaseModel):
    """Configuration for OCR processing."""
    include_bbox: bool = Field(default=False, description="Include bounding box information")
    crop_mode: bool = Field(default=True, description="Enable crop mode for better accuracy")
    prompt: Optional[str] = Field(default=None, description="Custom prompt for OCR processing")
    max_image_size: int = Field(default=4096, description="Maximum image size for processing")
    page_range: Optional[str] = Field(default=None, description="Page range for PDF processing (e.g., '1-5')")


class BoundingBox(BaseModel):
    """Bounding box information for detected elements."""
    x1: float = Field(description="Left coordinate")
    y1: float = Field(description="Top coordinate") 
    x2: float = Field(description="Right coordinate")
    y2: float = Field(description="Bottom coordinate")
    label: str = Field(description="Element type/label")
    confidence: Optional[float] = Field(default=None, description="Detection confidence score")


class OCRResult(BaseModel):
    """Result from OCR processing of a single page/image."""
    markdown_content: str = Field(description="Extracted content in Markdown format")
    processing_time: float = Field(description="Processing time in seconds")
    page_number: Optional[int] = Field(default=None, description="Page number for PDF files")
    bounding_boxes: Optional[List[BoundingBox]] = Field(default=None, description="Detected element bounding boxes")


class OCRResponse(BaseModel):
    """Complete response from OCR processing."""
    success: bool = Field(description="Whether processing was successful")
    file_type: str = Field(description="Type of processed file (image/pdf)")
    results: List[OCRResult] = Field(description="OCR results for each page/image")
    total_pages: Optional[int] = Field(default=None, description="Total number of pages processed")
    processing_time: float = Field(description="Total processing time in seconds")
    error_message: Optional[str] = Field(default=None, description="Error message if processing failed")


class ErrorResponse(BaseModel):
    """Error response format."""
    success: bool = Field(default=False, description="Always false for error responses")
    error_code: str = Field(description="Error code identifier")
    error_message: str = Field(description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="Service status")
    version: str = Field(description="Service version")
    model_loaded: bool = Field(description="Whether OCR model is loaded")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")


# Supported file formats
SUPPORTED_FORMATS = {
    FileType.IMAGE: ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'],
    FileType.PDF: ['.pdf']
}