"""The csv etl module"""
import pandas as pd

from life_expectancy.constant import FILEPATHS
from life_expectancy.country import Country
from life_expectancy.ETLs.base_etl import BaseETL


class CsvETL(BaseETL):
    """Reads data from csv and cleans it"""
    def __init__(self, filename : str=None, sep: str="\t") -> None:
        if filename is None:
            path = FILEPATHS()
            filename = path.csv_file_name
        self.filename = filename
        self.sep = sep

    def load_data(self) -> pd.DataFrame:
        """Loads the csv data

        :return: A pandas dataframe with the cleaned data
        :rtype: pd.DataFrame
        """
        return pd.read_csv(self.filename, sep=self.sep)

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
