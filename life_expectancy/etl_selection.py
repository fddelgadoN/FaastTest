"""Enum file for file extension to be read"""
from enum import Enum
from life_expectancy.etls.json import JsonETL
from life_expectancy.etls.csv import CsvETL
from life_expectancy.etls.base import BaseETL

class ETLSelection(Enum):
    """Enum class to filter file type"""
    JSON = JsonETL
    CSV = CsvETL

    @classmethod
    def from_path(cls, suffix: str) -> BaseETL:
        """Automatically checks the file extension

        :param suffix: the file extension
        :type suffix: str
        :raises ValueError: When the file extension is not permitted
        :return: the base etl class
        :rtype: BaseETL
        """
        for member in cls:
            if member.name.upper() == suffix.upper():
                return member.value
        raise ValueError(f"No member found with suffix {suffix}")
