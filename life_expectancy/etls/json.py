"""Module for json etl"""
import json

import pandas as pd

from life_expectancy.constant import FILEPATHS
from life_expectancy.country import Country
from life_expectancy.etls.base import BaseETL

class JsonETL(BaseETL):
    """Reads data from json and cleans it"""

    def __init__(self, filename : str=None) -> None:
        super().__init__()
        if filename is None:
            path = FILEPATHS()
            filename = path.json_file_name
        self.filename = filename

    def load_data(self) -> None:
        """Loads the json data"""
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.data = pd.DataFrame(json.load(file))

    def clean_data(self, country: Country) -> None:
        """Performs cleaning on the loaded data

        :param country: The country to filter by
        :type country: Country
        :param data: The previsously loaded data
        :type data: pd.DataFrame
        """
        self.data = self.data.rename(columns={'country': 'region', 'life_expectancy': 'value'})
        self.data = self.data.drop(columns=['flag', 'flag_detail'])

        if country is not None:
            self._filter_dataframe(country)
