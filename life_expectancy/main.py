"""Module to clean dataframe"""
import sys

import pandas as pd

from life_expectancy.cleaning import JSONCleaner, CSVCleaner
from life_expectancy.data_access import save_data

from life_expectancy.country import Country
from life_expectancy.file_type import FileExtension


def main(filename: str = None, file_type: FileExtension = FileExtension.CSV) -> pd.DataFrame:
    """Main function that calls all 3 functions

    Returns:
        pd.DataFrame: Cleaned dataframe
    """

    if file_type == FileExtension.CSV:
        cleaner = CSVCleaner(filename)
    elif file_type == FileExtension.JSON:
        cleaner = JSONCleaner(filename)

    country = sys.argv[-1]
    if cleaner.check_country_exists(country):
        country = Country[country.upper()].value
    else:
        country = Country.PT.value


    dataframe = cleaner.load_data()
    dataframe = cleaner.clean_data(country = country, data=dataframe)
    save_data(dataframe)
    return dataframe

if __name__ == "__main__": # pragma: no cover
    main()
