"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR


DATA_LOCATION = OUTPUT_DIR/"eu_life_expectancy_raw.tsv"
PT_FILE_NAME = OUTPUT_DIR/"pt_life_expectancy_expected.csv"

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
def data_cleaned() -> pd.DataFrame:
    """Fixture that loads cleans and saves the data for the tests

    Returns:
        pd.DataFrame: Cleaned data
    """
    return pd.read_csv(PT_FILE_NAME)


@pytest.fixture(scope="session")
def eu_csv_file() -> pd.DataFrame:
    """Read EU csv file
    Returns:
        pd. DataFrame: EU csv
    """
    return pd.read_csv(DATA_LOCATION, sep="\t")
