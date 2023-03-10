"""Module to clean dataframe"""
import sys

import pandas as pd

from life_expectancy.country import Country
from life_expectancy.etl_selection import ETLSelection

def main(filename: str = None, etl_type: ETLSelection = ETLSelection.CSV,
         country:str=None) -> pd.DataFrame:
    """Main function that calls all 3 functions

    Returns:
        pd.DataFrame: Cleaned dataframe
    """

    etl = ETLSelection.from_path(etl_type.name)(filename)


    if etl.check_country_exists(country):
        country = Country[country.upper()].value


    dataframe = etl.load_data()
    dataframe = etl.clean_data(country = country, data=dataframe)
    etl.save_data(dataframe)
    return dataframe

if __name__ == "__main__": # pragma: no cover
    main(country = sys.argv[-1])
