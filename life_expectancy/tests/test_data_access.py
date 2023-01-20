"""Test functions to test the data access functions"""
import pandas as pd
from life_expectancy import data_access

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"


def test_load_data(eu_csv_file : pd.DataFrame) -> None:
    """Test the load data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    data = data_access.load_data()
    assert pd.DataFrame.equals(eu_csv_file, data)
