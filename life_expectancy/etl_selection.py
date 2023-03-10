"""Enum file for file extension to be read"""
from enum import Enum
from life_expectancy.etls.json_etl import JsonETL
from life_expectancy.etls.csv_etl import CsvETL

class ETLSelection(Enum):
    """Enum class to filter file type"""
    JSON = JsonETL
    CSV = CsvETL
