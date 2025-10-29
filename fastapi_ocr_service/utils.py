"""Utility functions for the FastAPI OCR service."""

import os
import time
import uuid
from pathlib import Path
from typing import List, Optional, Tuple

from .models import FileType, SUPPORTED_FORMATS


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename with timestamp and UUID."""
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]
    file_extension = Path(original_filename).suffix.lower()
    return f"{timestamp}_{unique_id}{file_extension}"


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()


def get_file_type(filename: str) -> Optional[FileType]:
    """Determine file type based on extension."""
    extension = get_file_extension(filename)
    
    if extension in SUPPORTED_FORMATS[FileType.IMAGE]:
        return FileType.IMAGE
    elif extension in SUPPORTED_FORMATS[FileType.PDF]:
        return FileType.PDF
    else:
        return None


def is_supported_file_type(filename: str) -> bool:
    """Check if file type is supported."""
    return get_file_type(filename) is not None


def get_supported_extensions() -> List[str]:
    """Get list of all supported file extensions."""
    extensions = []
    for file_type in SUPPORTED_FORMATS:
        extensions.extend(SUPPORTED_FORMATS[file_type])
    return extensions


def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate file size against maximum allowed size."""
    return file_size <= max_size


def parse_page_range(page_range: Optional[str], total_pages: int) -> List[int]:
    """Parse page range string and return list of page numbers."""
    if not page_range:
        return list(range(1, total_pages + 1))
    
    pages = []
    try:
        for part in page_range.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages.extend(range(max(1, start), min(total_pages + 1, end + 1)))
            else:
                page_num = int(part)
                if 1 <= page_num <= total_pages:
                    pages.append(page_num)
    except ValueError:
        # If parsing fails, return all pages
        return list(range(1, total_pages + 1))
    
    return sorted(list(set(pages)))  # Remove duplicates and sort


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def ensure_directory_exists(directory_path: str) -> None:
    """Ensure directory exists, create if it doesn't."""
    os.makedirs(directory_path, exist_ok=True)


def cleanup_file(file_path: str) -> bool:
    """Clean up a single file. Returns True if successful."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except OSError:
        pass
    return False


def get_file_info(file_path: str) -> dict:
    """Get file information including size and modification time."""
    try:
        stat = os.stat(file_path)
        return {
            "size": stat.st_size,
            "modified": stat.st_mtime,
            "exists": True
        }
    except OSError:
        return {"exists": False}