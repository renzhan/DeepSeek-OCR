"""Application state management for the FastAPI OCR service."""

from typing import Optional
from .config import Settings


class AppState:
    """Global application state."""
    
    def __init__(self):
        self.ocr_engine: Optional[object] = None
        self.settings: Optional[Settings] = None
        self.is_initialized: bool = False
        self.model_loaded: bool = False
        
        # Statistics
        self.request_count: int = 0
        self.processing_time_total: float = 0.0
        self.error_count: int = 0
        self.image_requests: int = 0
        self.pdf_requests: int = 0
    
    def initialize(self, settings: Settings) -> None:
        """Initialize application state with settings."""
        self.settings = settings
        self.is_initialized = True
    
    def set_ocr_engine(self, engine: object) -> None:
        """Set the OCR engine instance."""
        self.ocr_engine = engine
        self.model_loaded = True
    
    def increment_request_count(self) -> None:
        """Increment total request count."""
        self.request_count += 1
    
    def increment_error_count(self) -> None:
        """Increment error count."""
        self.error_count += 1
    
    def add_processing_time(self, processing_time: float) -> None:
        """Add processing time to total."""
        self.processing_time_total += processing_time
    
    def increment_image_requests(self) -> None:
        """Increment image request count."""
        self.image_requests += 1
    
    def increment_pdf_requests(self) -> None:
        """Increment PDF request count."""
        self.pdf_requests += 1
    
    @property
    def average_processing_time(self) -> float:
        """Calculate average processing time."""
        if self.request_count == 0:
            return 0.0
        return self.processing_time_total / self.request_count
    
    @property
    def error_rate(self) -> float:
        """Calculate error rate as percentage."""
        if self.request_count == 0:
            return 0.0
        return (self.error_count / self.request_count) * 100
    
    def get_stats(self) -> dict:
        """Get application statistics."""
        return {
            "request_count": self.request_count,
            "error_count": self.error_count,
            "error_rate": self.error_rate,
            "average_processing_time": self.average_processing_time,
            "image_requests": self.image_requests,
            "pdf_requests": self.pdf_requests,
            "model_loaded": self.model_loaded,
            "is_initialized": self.is_initialized
        }


# Global app state instance
app_state = AppState()