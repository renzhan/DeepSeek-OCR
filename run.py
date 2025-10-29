#!/usr/bin/env python3
"""Run script for FastAPI OCR Service."""

import uvicorn
from fastapi_ocr_service.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "fastapi_ocr_service.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )