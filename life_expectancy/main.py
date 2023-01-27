"""Module to clean dataframe"""
import sys

import pandas as pd

from life_expectancy.cleaning import JSONCleaner, CSVCleaner
from life_expectancy.data_access import save_data

from .country import Country
from .file_type import FileExtension


def main(file_type: FileExtension = FileExtension.CSV) -> pd.DataFrame:
    """Main function that calls all 3 functions

    Returns:
        pd.DataFrame: Cleaned dataframe
    """

    country = sys.argv[-1]
    if country.upper() in Country.__members__:
        country = Country[country.upper()].value
    else:
        country = Country.PT.value

    if file_type == FileExtension.CSV:
        cleaner = CSVCleaner()
    elif file_type == FileExtension.JSON:
        cleaner = JSONCleaner()
    dataframe = cleaner.load_data()
    dataframe = cleaner.clean_data(country = country, data=dataframe)
    save_data(dataframe)
    return dataframe

if __name__ == "__main__": # pragma: no cover
    main()
