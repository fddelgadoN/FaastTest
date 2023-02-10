"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR

DATA_LOCATION_CSV = OUTPUT_DIR/"eu_life_expectancy_raw.tsv"
DATA_LOCATION_JSON = OUTPUT_DIR/"eurostat_life_expect.json"
PT_FILE_NAME = OUTPUT_DIR/"pt_life_expectancy_expected.csv"
EU_FILE_NAME = OUTPUT_DIR/"eu_life_expectancy_expected.csv"

PT_FILE_NAME_JSON = OUTPUT_DIR/"pt_life_expectancy_expected_json.csv"

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
    return pd.read_csv(PT_FILE_NAME)


@pytest.fixture(scope="session")
def data_cleaned_json() -> pd.DataFrame:
    """Fixture that reads the csv file cleaned through the json loader

    Returns:
        pd.DataFrame: Cleaned data
    """
    return pd.read_csv(PT_FILE_NAME_JSON)

@pytest.fixture(scope="session")
def eu_csv_file() -> pd.DataFrame:
    """Loads CSV file with all info

    Returns:
        pd.DataFrame: Loaded data
    """
    return pd.read_csv(DATA_LOCATION_CSV, sep="\t")
