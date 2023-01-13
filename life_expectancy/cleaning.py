"""Module to clean dataframe"""
import sys
from typing import List

import pandas as pd

from life_expectancy.data_access import load_data, save_data

def _unpivot_year_columns(data: pd.DataFrame) -> pd.DataFrame:
    years_cols = [x for x in data.columns if x.strip().isnumeric()]
    data = pd.melt(data, id_vars=data.columns[0], value_vars=years_cols, \
        value_name='value', var_name='year')
    return data

def _filter_dataframe(data:pd.DataFrame, country:str) -> pd.DataFrame:
    return data.loc[data.region.str.upper() == country.upper()]

def _process_columns(data: pd.DataFrame, column: str, col_index: int) -> pd.DataFrame:
    data = data.rename(columns={column: column.partition('\\')[0]})
    data = _unpivot_year_columns(data)
    data[data.columns[col_index].split(",")] = [x.split(',') for x in data.iloc[:, col_index]]
    data = data.rename(columns={'geo': 'region'})

    return data

def clean_data(
        argv : List[str],
        data: pd.DataFrame) -> pd.DataFrame:
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
        data (pd.DataFrame): Unprocessed data read from file contain info about the countries

    Returns:
        pd.DataFrame: Dataframe processed and filtered by the required country (if needed)
    """

    assert data is not None, "Error extracting data is null"

    #process column values
    data = _process_columns(data, data.columns[0], 0)

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
    if len(argv)>0:
        country = argv[0]
        data = _filter_dataframe(data, country)

    return data

def main() -> pd.DataFrame:
    """Main function that calls all 3 functions

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    dataframe = load_data()
    dataframe = clean_data(argv = sys.argv[1:], data=dataframe)
    save_data(dataframe)
    return dataframe

if __name__ == "__main__": # pragma: no cover
    main()
