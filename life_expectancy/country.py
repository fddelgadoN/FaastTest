"""Enum file"""
from enum import Enum

class Country(str, Enum):
    """Enum class to remove possible errors from input"""
    PT = "PT"
    EE = "EE"
