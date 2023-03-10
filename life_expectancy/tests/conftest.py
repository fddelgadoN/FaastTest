"""Pytest configuration file"""
import json

import pandas as pd
import pytest
from life_expectancy.tests.path_tests import FilePathsTest

from . import FIXTURES_DIR, OUTPUT_DIR

PATHS = FilePathsTest(OUTPUT_DIR)

@pytest.fixture(autouse=True)
def run_before_and_after_tests() -> None:
    """Fixture to execute commands before and after a test is run"""
    # Setup: fill with any logic you want

    yield # this is where the testing happens

    # Teardown : fill with any logic you want
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    file_path.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")


@pytest.fixture(scope="session")
def data_cleaned_csv() -> pd.DataFrame:
    """Fixture that reads the csv file cleaned through the csv loader

    Returns:
        pd.DataFrame: Cleaned data
    """
    return pd.read_csv(PATHS.pt_file_name_csv)


@pytest.fixture(scope="session")
def data_cleaned_json() -> pd.DataFrame:
    """Fixture that reads the csv file cleaned through the json loader

    Returns:
        pd.DataFrame: Cleaned data
    """
    return pd.read_csv(PATHS.pt_file_name_json)

@pytest.fixture(scope="session")
def eu_csv_file() -> pd.DataFrame:
    """Loads CSV file with all info

    Returns:
        pd.DataFrame: Loaded data
    """
    return pd.read_csv(PATHS.data_location_csv, sep="\t")


@pytest.fixture(scope="session")
def eu_json_file() -> pd.DataFrame:
    """Loads CSV file with all info

    Returns:
        pd.DataFrame: Loaded data
    """
    with open(PATHS.data_location_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return pd.DataFrame(data)
