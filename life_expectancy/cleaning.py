"""Cleaning file with objects to clean various types of file extensions"""
from abc import ABC

import pandas as pd
from life_expectancy.data_access import Loader, CSVLoader, JSONLoader
from .country import Country

class Cleaner(ABC):
    """Cleaner object for various types of files"""
    def __init__(self, filename : str = None) -> None:
        self.loader = Loader(filename)

    def clean_data(self, country : Country, data: pd.DataFrame) -> pd.DataFrame:
        """Cleans data
        Args:
            country (Country): name of country to filter data
            data (pd.DataFrame): data object

        Returns:
            pd.DataFrame: cleaned final data
        """

    def load_data(self) -> pd.DataFrame:
        """Loads the data from file

        Returns:
            pd.DataFrame: dataframe with loaded data
        """
        return self.loader.load_data()

    def _filter_dataframe(self, data:pd.DataFrame, country:str) -> pd.DataFrame:
        return data.loc[data.region.str.upper() == country.upper()]

class CSVCleaner(Cleaner):
    """Reads data from csv and cleans it"""
    def __init__(self, filename : str=None) -> None:
        super().__init__(filename)
        self.loader = CSVLoader(filename)

    def _unpivot_year_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        years_cols = [x for x in data.columns if x.strip().isnumeric()]
        data = pd.melt(data, id_vars=data.columns[0], value_vars=years_cols, \
            value_name='value', var_name='year')
        return data


    def _process_columns(self, data: pd.DataFrame, column: str, col_index: int) -> pd.DataFrame:
        data = data.rename(columns={column: column.partition('\\')[0]})
        data = self._unpivot_year_columns(data)
        data[data.columns[col_index].split(",")] = [x.split(',') for x in data.iloc[:, col_index]]
        data = data.rename(columns={'geo': 'region'})

        return data

    def clean_data(self, country: Country, data: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe and save it to file.
            Firstly removing the backslash from columns names.
            Unpivotting the year columns to be in a single column
            Splitting the comma separated columns
            Renaming columns to expected form and reordering the columns
            Removing nonsense values from value column
            Changing the dtypes
            And if needed filtering out to a certain country
            Args:
                argv (List[str]): List of country abbreviations to filter by
                data (pd.DataFrame): Unprocessed data read from file with info about the countries

            Returns:
                pd.DataFrame: Dataframe processed and filtered by the required country (if needed)
        """
        assert data is not None, "Error extracting data is null"

        #process column values
        data = self._process_columns(data, data.columns[0], 0)

        #Reorder columns to fit to expected output...
        data=data[['unit','sex','age','region','year','value']]

        #Remove thrash from value column and filter out empty values
        data['value'] = data['value'].str.replace(r'[^\d\.]', '')
        data = data.drop(data[data['value'] == ''].index)

        #Convert needed dtypes
        data = data.astype({
            'year' : 'int64',
            'value' : 'float'
        })

        #Filter to only received region
        if country is not None:
            data = self._filter_dataframe(data, country)

        return data

class JSONCleaner(Cleaner):
    """Reads data from json and cleans it"""

    def __init__(self, filename : str=None) -> None:
        super().__init__(filename)
        self.loader = JSONLoader(filename)

    def clean_data(self, country: Country, data: pd.DataFrame) -> pd.DataFrame:
        data = data.rename(columns={'country': 'region', 'life_expectancy': 'value'})
        data = data.drop(columns=['flag', 'flag_detail'])

        if country is not None:
            data = self._filter_dataframe(data, country)

        return data
