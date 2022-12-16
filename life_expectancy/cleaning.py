"""Module to clean dataframe"""
import sys
from typing import List

import pandas as pd

from .loaders import load_data, save_data

def _split_comma_separated_column(data: pd.DataFrame, column:int) -> pd.DataFrame:
    data[data.columns[column].split(",")] = [x.split(',') for x in data.iloc[:, column]]
    return data

def _unpivot_year_columns(data: pd.DataFrame) -> pd.DataFrame:
    years_cols = [x for x in data.columns if x.strip().isnumeric()]
    data = pd.melt(data, id_vars=data.columns[0], value_vars=years_cols, \
        value_name='value', var_name='year')
    return data

def _drop_backslash_from_column_name(data:pd.DataFrame, column:str) -> pd.DataFrame:
    return data.rename(columns={column: column.partition('\\')[0]})

def _filter_dataframe(data:pd.DataFrame, country:str) -> pd.DataFrame:
    return data.loc[data.region.str.upper() == country.upper()]

def clean_data(
        argv : List[str],
        data: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe and save it to file"""
    assert data is not None, "Error extracting data is null"

    #Drop irrelevant info from first column
    data = _drop_backslash_from_column_name(data, data.columns[0])

    #Unpivot the year columns
    data = _unpivot_year_columns(data)

    #Split first column that is comma separated
    data = _split_comma_separated_column(data, 0)
    data = data.rename(columns={'geo': 'region'})

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

if __name__ == "__main__": # pragma: no cover
    dataframe = load_data()
    dataframe = clean_data(argv = sys.argv[1:], data=dataframe)
    save_data(dataframe)
