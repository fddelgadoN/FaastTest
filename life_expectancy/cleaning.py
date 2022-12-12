"""Module to clean dataframe"""
import sys
from typing import List

import pandas as pd

# pylint: disable=import-error
from utils import (change_dtypes, drop_backslash_from_column_name,
                   split_comma_separated_column, unpivot_year_columns)
from file_manipulation import save_data, load_data
# pylint: enable=import-error

def clean_data(
        argv : List[str],
        data: pd.DataFrame) -> pd.DataFrame:
    """Clean dataframe and save it to file"""
    assert data is not None, "Error extracting data is null"

    country = argv[0]

    #Drop irrelevant info from first column
    data = drop_backslash_from_column_name(data, data.columns[0])

    #Unpivot the year columns
    data = unpivot_year_columns(data)

    #Split first column that is comma separated
    data = split_comma_separated_column(data, 0)
    data = data.rename(columns={'geo': 'region'})

    #Reorder columns to fit to expected output...
    data=data[['unit','sex','age','region','year','value']]

    #Remove thrash from value column and filter out empty values
    data['value'] = data['value'].str.replace(r'[^\d\.]', '')
    data = data.drop(data[data['value'] == ''].index)

    #Convert needed dtypes
    data = change_dtypes(data,
    {
        'year' : 'int64',
        'value' : 'float'
    })

    #Filter to only received region
    data = data.loc[data.region.str.upper() == country.upper()]

    return data

if __name__ == "__main__": # pragma: no cover
    dataframe = load_data()
    dataframe = clean_data(argv = sys.argv[1:], data=dataframe)
    save_data(dataframe)
