"""Utils module with complementary functions"""
from typing import Dict
import pandas as pd


def split_comma_separated_column(data: pd.DataFrame) -> pd.DataFrame:
    """Split comma separated column"""
    data[data.columns[0].split(",")] = [x.split(',') for x in data.iloc[:, 0]]
    return data

def change_dtypes(data: pd.DataFrame, dtypes: Dict[str, str]) -> pd.DataFrame:
    """Change dtypes receiving dict with name and dtype"""
    return data.astype(dtypes)

def unpivot_year_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Unpivot columns that are int i.e. years"""
    years_cols = [x for x in data.columns if x.strip().isnumeric()]
    data = pd.melt(data, id_vars=data.columns[0], value_vars=years_cols, \
        value_name='value', var_name='year')
    return data

def drop_backslash_from_column_name(data:pd.Dataframe, column:str) -> pd.DataFrame:
    """Remove starting from the backslash"""
    return data.rename(columns={column: column.partition('\\')[0]})
    