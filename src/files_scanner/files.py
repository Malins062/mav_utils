import os
import zlib
from datetime import datetime

from loguru import logger


def calculate_crc32(file_path):
    """Calculate CRC32 checksum for a file"""
    try:
        prev = 0
        with open(file_path, "rb") as f:
            for line in f:
                prev = zlib.crc32(line, prev)
        return f"{prev & 0xFFFFFFFF:08X}"
    except Exception as e:
        logger.error(f"Error calculating CRC32 for {file_path}: {e}")
        return f"ERROR: {str(e)}"


def get_file_size(file_path):
    """Get file size"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes
    except Exception as e:
        logger.warning(f"Error getting size for {file_path}: {e}")
        return 0


def get_file_date(file_path):
    """Get file modification date"""
    try:
        timestamp = os.path.getmtime(file_path)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        logger.warning(f"Error getting date for {file_path}: {e}")
        return "Unknown"
