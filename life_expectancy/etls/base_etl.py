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

    @abstractmethod
    def clean_data(self, country : Country, data: pd.DataFrame) -> pd.DataFrame:
        """Cleans data
        Args:
            country (Country): name of country to filter data
            data (pd.DataFrame): data object

        Returns:
            pd.DataFrame: cleaned final data
        """

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads the data from file

        Returns:
            pd.DataFrame: dataframe with loaded data
        """

    @staticmethod
    def _filter_dataframe(data:pd.DataFrame, country:Country) -> pd.DataFrame:
        return data.loc[data.region.str.upper() == country.upper()]

    @staticmethod
    def save_data(data:pd.DataFrame, save_location:str = path.data_folder) -> None:
        """Save the data to file"""
        data.to_csv(save_location, index=False)


    @staticmethod
    def check_country_exists(country: str) -> bool:
        """Test if the country receives is possible
        Args:
            country (Country): Country received
        Returns:
            bool: True or false based on if it exists
        """
        if country is not None and country.upper() in Country.__members__:
            return True
        return False
