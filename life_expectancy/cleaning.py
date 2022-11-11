"""Module to clean dataframe"""
import sys
from typing import List

import pandas as pd

def clean_data(argv : List[str],
file_name : str = 'eu_life_expectancy_raw.tsv', saved_file: str = "pt_life_expectancy.csv") -> None:
    """Clean dataframe and save it to file"""

    country = argv[0]

    data_location = "life_expectancy/data/"
    data = pd.read_csv(data_location+file_name,sep='\t')

    #Drop irrelevant info from first column
    data = data.rename(columns={data.columns[0]: data.columns[0].partition('\\')[0]})

    #Unpivot data
    years_cols = [x for x in data.columns if x.strip().isnumeric()]
    data = pd.melt(data, id_vars=data.columns[0], value_vars=years_cols, \
        value_name='value', var_name='year')

    #Split first column that is comma separated
    data[data.columns[0].split(",")] = [x.split(',') for x in data.iloc[:, 0]]
    data['region'] = data['geo']
    data = data.drop([data.columns[0], 'geo'], axis=1)

    #Reorder columns to fit to expected output...
    data=data[['unit','sex','age','region','year','value']]

    #Remove thrash from value column and filter out empty values
    data['value'] = data['value'].str.replace(r'[^\d\.]', '')
    data = data.drop(data[data['value'] == ''].index)

    #Convert needed dtypes
    data['year'] = data.year.astype('int64')
    data['value'] = data.value.astype('float')

    #Filter to only pt region
    data = data.loc[data.region == country.upper()]

    #Save to file
    data.to_csv(data_location+saved_file, index=False)

if __name__ == "__main__": # pragma: no cover
    clean_data(argv = sys.argv[1:], file_name = "eu_life_expectancy_raw.tsv")
