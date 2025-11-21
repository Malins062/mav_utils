import zlib
from datetime import datetime
from pathlib import Path

from loguru import logger


def calculate_crc32(file_path):
    """Calculate CRC32 checksum for a file"""
    try:
        prev = 0
        path = Path(file_path)
        with path.open("rb") as f:
            for line in f:
                prev = zlib.crc32(line, prev)
        return f"{prev & 0xFFFFFFFF:08X}"
    except Exception as e:
        logger.error(f"Error calculating CRC32 for {file_path}: {e}")
        return f"ERROR: {str(e)}"


def get_file_size(file_path):
    """Get file size"""
    try:
        path = Path(file_path)
        size_bytes = path.stat().st_size
        return size_bytes
    except Exception as e:
        logger.warning(f"Error getting size for {file_path}: {e}")
        return 0


def get_file_date(file_path):
    """Get file modification date"""
    try:
        path = Path(file_path)
        timestamp = path.stat().st_mtime
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.warning(f"Error getting date for {file_path}: {e}")
        return "Unknown"


def get_filename_without_extension(filepath: str) -> str:
    """
    Возвращает имя файла без расширения
    """
    return Path(filepath).stem
