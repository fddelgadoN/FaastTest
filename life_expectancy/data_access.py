"""Save and load functions
"""
from abc import ABC
import json
import pandas as pd

from life_expectancy.constant import SAVED_FILE, JSON_FILE_NAME, CSV_FILE_NAME


class Loader(ABC):
    """Factory Loader to load certain files extension"""
    def __init__(self, file_name:str):
        self.file_name = file_name

    def load_data(self):
        """Load the data into a pd"""

    def get_file_name(self) -> str:
        """Get file name

        Returns:
            str: file name that was loaded
        """
        return self.file_name

class CSVLoader(Loader):
    """Loads the data from a csv"""
    def __init__(self, file_name: str, sep: str="\t"):
        if file_name is None:
            file_name = CSV_FILE_NAME

        super().__init__(file_name)
        self.sep = sep

    def load_data(self) -> pd.DataFrame:
        """Load the data into a pd"""
        return pd.read_csv(self.file_name, sep=self.sep)

class JSONLoader(Loader):
    """Loads the data from a json"""
    def __init__(self, file_name: str):
        if file_name is None:
            file_name = JSON_FILE_NAME
        super().__init__(file_name)

    def load_data(self) -> pd.DataFrame:
        """Load the data into a pd"""
        with open(self.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return pd.DataFrame(data)


def save_data(data:pd.DataFrame, save_location:str = SAVED_FILE) -> None:
    """Save the data to file"""
    data.to_csv(save_location, index=False)
