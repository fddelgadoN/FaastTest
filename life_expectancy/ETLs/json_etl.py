"""Module for json etl"""
import json

import pandas as pd

from life_expectancy.constant import FILEPATHS
from life_expectancy.country import Country
from life_expectancy.ETLs.base_etl import BaseETL

class JsonETL(BaseETL):
    """Reads data from json and cleans it"""

    def __init__(self, filename : str=None) -> None:
        if filename is None:
            path = FILEPATHS()
            filename = path.json_file_name
        self.filename = filename

    def load_data(self) -> pd.DataFrame:
        """Loads the json data

        :return: A pandas dataframe with loaded data
        :rtype: pd.DataFrame
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return pd.DataFrame(data)

    def clean_data(self, country: Country, data: pd.DataFrame) -> pd.DataFrame:
        """Performs cleaning on the loaded data

        :param country: The country to filter by
        :type country: Country
        :param data: The previsously loaded data
        :type data: pd.DataFrame
        :return: The cleaned data
        :rtype: pd.DataFrame
        """
        data = data.rename(columns={'country': 'region', 'life_expectancy': 'value'})
        data = data.drop(columns=['flag', 'flag_detail'])

        if country is not None:
            data = self._filter_dataframe(data, country)

        return data
