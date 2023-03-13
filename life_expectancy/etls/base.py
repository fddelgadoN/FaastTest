"""
Base ETL module that is the abstract class for all other etl classes

As of now supports the following file extensions: .json, .csv
"""
from abc import ABC, abstractmethod

import pandas as pd

from life_expectancy.constant import FILEPATHS
from life_expectancy.country import Country

path = FILEPATHS()

class BaseETL(ABC):
    """Base ETL class"""
    def __init__(self) -> None:
        self.data = pd.DataFrame()

    @abstractmethod
    def clean_data(self, country : Country, data: pd.DataFrame) -> pd.DataFrame:
        """Cleans data
        Args:
            country (Country): name of country to filter data
            data (pd.DataFrame): data object

        Returns:
            pd.DataFrame: cleaned final data
        """
        ...

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads the data from file

        Returns:
            pd.DataFrame: dataframe with loaded data
        """
        ...

    def _filter_dataframe(self, country:Country) -> pd.DataFrame:
        self.data = self.data.loc[self.data.region.str.upper() == country.upper()]

    def save_data(self, save_location:str = path.data_folder) -> None:
        """Save the data to file"""
        self.data.to_csv(save_location, index=False)
