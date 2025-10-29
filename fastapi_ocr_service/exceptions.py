"""Custom exceptions for the FastAPI OCR service."""

from typing import Any, Dict, Optional


class OCRServiceException(Exception):
    """Base exception for OCR service errors."""
    
    def __init__(
        self,
        message: str,
        error_code: str = "OCR_ERROR",
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)


class FileValidationError(OCRServiceException):
    """Exception raised when file validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="FILE_VALIDATION_ERROR",
            details=details,
            status_code=400
        )


class UnsupportedFileTypeError(OCRServiceException):
    """Exception raised when file type is not supported."""
    
    def __init__(self, file_type: str, supported_types: list):
        message = f"Unsupported file type: {file_type}. Supported types: {', '.join(supported_types)}"
        super().__init__(
            message=message,
            error_code="UNSUPPORTED_FILE_TYPE",
            details={"file_type": file_type, "supported_types": supported_types},
            status_code=400
        )


class FileSizeExceededError(OCRServiceException):
    """Exception raised when file size exceeds the limit."""
    
    def __init__(self, file_size: int, max_size: int):
        message = f"File size {file_size} bytes exceeds maximum allowed size {max_size} bytes"
        super().__init__(
            message=message,
            error_code="FILE_SIZE_EXCEEDED",
            details={"file_size": file_size, "max_size": max_size},
            status_code=413
        )


class ModelNotLoadedError(OCRServiceException):
    """Exception raised when OCR model is not loaded."""
    
    def __init__(self):
        super().__init__(
            message="OCR model is not loaded. Please wait for model initialization.",
            error_code="MODEL_NOT_LOADED",
            status_code=503
        )


class OCRProcessingError(OCRServiceException):
    """Exception raised when OCR processing fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"OCR processing failed: {message}",
            error_code="OCR_PROCESSING_ERROR",
            details=details,
            status_code=500
        )


class FileCorruptedError(OCRServiceException):
    """Exception raised when file is corrupted or cannot be processed."""
    
    def __init__(self, message: str = "File is corrupted or cannot be processed"):
        super().__init__(
            message=message,
            error_code="FILE_CORRUPTED",
            status_code=422
        )


class InsufficientStorageError(OCRServiceException):
    """Exception raised when there's insufficient storage space."""
    
    def __init__(self):
        super().__init__(
            message="Insufficient storage space for processing",
            error_code="INSUFFICIENT_STORAGE",
            status_code=507
        )