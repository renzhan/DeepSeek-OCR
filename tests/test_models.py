"""Tests for data models."""

import pytest
from datetime import datetime
from fastapi_ocr_service.models import (
    OCRConfig, BoundingBox, OCRResult, OCRResponse, 
    ErrorResponse, HealthResponse, FileType, SUPPORTED_FORMATS
)


def test_ocr_config_defaults():
    """Test OCRConfig default values."""
    config = OCRConfig()
    assert config.include_bbox is False
    assert config.crop_mode is True
    assert config.prompt is None
    assert config.max_image_size == 4096
    assert config.page_range is None


def test_ocr_config_custom():
    """Test OCRConfig with custom values."""
    config = OCRConfig(
        include_bbox=True,
        crop_mode=False,
        prompt="Custom prompt",
        max_image_size=2048,
        page_range="1-5"
    )
    assert config.include_bbox is True
    assert config.crop_mode is False
    assert config.prompt == "Custom prompt"
    assert config.max_image_size == 2048
    assert config.page_range == "1-5"


def test_bounding_box():
    """Test BoundingBox model."""
    bbox = BoundingBox(
        x1=10.0,
        y1=20.0,
        x2=100.0,
        y2=200.0,
        label="title",
        confidence=0.95
    )
    assert bbox.x1 == 10.0
    assert bbox.y1 == 20.0
    assert bbox.x2 == 100.0
    assert bbox.y2 == 200.0
    assert bbox.label == "title"
    assert bbox.confidence == 0.95


def test_ocr_result():
    """Test OCRResult model."""
    result = OCRResult(
        markdown_content="# Test Content",
        processing_time=1.5,
        page_number=1,
        bounding_boxes=[
            BoundingBox(x1=0, y1=0, x2=100, y2=50, label="title")
        ]
    )
    assert result.markdown_content == "# Test Content"
    assert result.processing_time == 1.5
    assert result.page_number == 1
    assert len(result.bounding_boxes) == 1


def test_ocr_response():
    """Test OCRResponse model."""
    response = OCRResponse(
        success=True,
        file_type="image",
        results=[
            OCRResult(markdown_content="# Test", processing_time=1.0)
        ],
        total_pages=1,
        processing_time=1.2
    )
    assert response.success is True
    assert response.file_type == "image"
    assert len(response.results) == 1
    assert response.total_pages == 1
    assert response.processing_time == 1.2
    assert response.error_message is None


def test_error_response():
    """Test ErrorResponse model."""
    error = ErrorResponse(
        error_code="TEST_ERROR",
        error_message="Test error message",
        details={"key": "value"}
    )
    assert error.success is False
    assert error.error_code == "TEST_ERROR"
    assert error.error_message == "Test error message"
    assert error.details == {"key": "value"}
    assert isinstance(error.timestamp, datetime)


def test_health_response():
    """Test HealthResponse model."""
    health = HealthResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=True
    )
    assert health.status == "healthy"
    assert health.version == "1.0.0"
    assert health.model_loaded is True
    assert isinstance(health.timestamp, datetime)


def test_file_type_enum():
    """Test FileType enum."""
    assert FileType.IMAGE == "image"
    assert FileType.PDF == "pdf"


def test_supported_formats():
    """Test SUPPORTED_FORMATS constant."""
    assert FileType.IMAGE in SUPPORTED_FORMATS
    assert FileType.PDF in SUPPORTED_FORMATS
    assert '.jpg' in SUPPORTED_FORMATS[FileType.IMAGE]
    assert '.pdf' in SUPPORTED_FORMATS[FileType.PDF]