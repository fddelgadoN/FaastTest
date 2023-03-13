"""The csv etl module"""
import pandas as pd

from life_expectancy.constant import FILEPATHS
from life_expectancy.country import Country
from life_expectancy.etls.base import BaseETL


class CsvETL(BaseETL):
    """Reads data from csv and cleans it"""
    def __init__(self, filename : str=None, sep: str="\t") -> None:
        super().__init__()
        if filename is None:
            path = FILEPATHS()
            filename = path.csv_file_name
        self.filename = filename
        self.sep = sep

    def load_data(self) -> None:
        """Loads the csv data"""
        self.data = pd.read_csv(self.filename, sep=self.sep)

    def _unpivot_year_columns(self) -> None:
        years_cols = [x for x in self.data.columns if x.strip().isnumeric()]
        self.data = pd.melt(self.data, id_vars=self.data.columns[0], value_vars=years_cols, \
            value_name='value', var_name='year')


    def _process_columns(self, column: str, col_index: int) -> None:
        self.data = self.data.rename(columns={column: column.partition('\\')[0]})
        self._unpivot_year_columns()
        self.data[self.data.columns[col_index].split(",")] = [x.split(',') for x in self.data.iloc[:, col_index]]
        self.data = self.data.rename(columns={'geo': 'region'})

    def clean_data(self, country: Country) -> None:
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
        """
        assert self.data is not None, "Error extracting data is null"

        #process column values
        self._process_columns(self.data.columns[0], 0)

        #Reorder columns to fit to expected output...
        self.data=self.data[['unit','sex','age','region','year','value']]

        #Remove thrash from value column and filter out empty values
        self.data['value'] = self.data['value'].str.replace(r'[^\d\.]', '')
        self.data = self.data.drop(self.data[self.data['value'] == ''].index)

        #Convert needed dtypes
        self.data = self.data.astype({
            'year' : 'int64',
            'value' : 'float'
        })

        #Filter to only received region
        if country is not None:
            self._filter_dataframe(country)
