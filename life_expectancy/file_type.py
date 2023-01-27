"""Enum file for file extension to be read"""
from enum import Enum

class FileExtension(str, Enum):
    """Enum class to filter file type"""
    JSON = "json"
    CSV = "csv"
