# FastAPI OCR Service

A FastAPI-based OCR service that uses DeepSeek OCR-VLLM for processing PDF and image files, converting them to Markdown format with optional bounding box information.

## Features

- **Unified API**: Single endpoint for both PDF and image processing
- **Automatic File Type Detection**: Automatically detects file type based on extension
- **Markdown Output**: Converts OCR results to structured Markdown format
- **Optional Bounding Boxes**: Provides element position information when requested
- **Synchronous Processing**: Direct response without async task management
- **Comprehensive Error Handling**: Detailed error responses and logging

## Supported File Types

- **Images**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`
- **PDFs**: `.pdf`

## Quick Start

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment configuration:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` file with your configuration

### Running the Service

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn fastapi_ocr_service.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### OCR Processing
- **POST** `/api/v1/ocr`
  - Upload a file for OCR processing
  - Parameters:
    - `file`: File to process (PDF or image)
    - `include_bbox`: Include bounding box information (optional, default: false)
    - `crop_mode`: Enable crop mode for better accuracy (optional, default: true)
    - `prompt`: Custom prompt for OCR processing (optional)
    - `page_range`: Page range for PDF files (optional, e.g., "1-5")

### Health Check
- **GET** `/api/v1/health`
  - Check service health and status

## Configuration

The service can be configured using environment variables. See `.env.example` for all available options.

Key configuration options:
- `OCR_MODEL_PATH`: Path to DeepSeek OCR model
- `OCR_MAX_FILE_SIZE`: Maximum file size in bytes
- `OCR_TEMP_DIR`: Temporary file storage directory
- `OCR_LOG_LEVEL`: Logging level

## Development Status

This is currently under development. The following tasks are completed:

- [x] Project structure and core interfaces
- [ ] OCR engine implementation
- [ ] File handling and validation
- [ ] API endpoints
- [ ] Error handling and logging
- [ ] Configuration management
- [ ] Performance optimization
- [ ] Documentation and deployment

## License

[Add your license information here]