"""Test cleaning functions"""
from unittest.mock import patch

import pandas as pd
import pytest

from life_expectancy.main import main
from life_expectancy.country import Country
from life_expectancy.etl_selection import ETLSelection
from life_expectancy.etls.csv import CsvETL
from life_expectancy.etls.json import JsonETL


EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"
EU_FILE_NAME_JSON = "life_expectancy/data/eu_life_expectancy_expected_json.csv"

class MockCsvETL(CsvETL):
    """Mock ETL with data equal to fixture"""
    def load_data(self):
        """Loads the fixture into data"""
        self.data = pd.read_csv(EU_FILE_NAME, ",")
    def save_data(self, _: str = "") -> None:
        print("MonkeyPatch Save")

@patch("life_expectancy.main.ETLSelection.from_path", return_value=MockCsvETL)
def test_main_csv(_ : pytest.MonkeyPatch, data_cleaned_csv: pd.DataFrame, capfd) -> None:
    """Test the main function that loads, cleans and saves the data, using a mock etl class that
    uses the fixtures and does not save. Checking aswell if save_data is called

    Args:
        monkeypatch (Monkeypatch): MonkeyPatch object
        data_cleaned_csv (Fixture): Data fixture with cleaned data
    """
    data = main(country=Country.PT).reset_index(drop=True)
    assert pd.DataFrame.equals(data, data_cleaned_csv)
    out, _ = capfd.readouterr()
    assert out == "MonkeyPatch Save\n"


class MockJsonETL(JsonETL):
    """Mock ETL with data equal to fixture"""
    def load_data(self):
        """Loads the fixture into data"""
        self.data = pd.read_csv(EU_FILE_NAME_JSON, ",")
    def save_data(self, _: str = "") -> None:
        print("MonkeyPatch Save")

@patch("life_expectancy.main.ETLSelection.from_path", return_value=MockJsonETL)
def test_main_json(_ : pytest.MonkeyPatch,
            data_cleaned_json: pd.DataFrame, capfd) -> None:
    """Test the main function that loads, cleans and saves the data, using a mock etl class that
    uses the fixtures and does not save. Checking aswell if save_data is called

    Args:
        monkeypatch (Monkeypatch): MonkeyPatch object
        data_cleaned_json (Fixture): Data fixture with cleaned data
    """

    data = main(etl_type = ETLSelection.JSON, country=Country.PT).reset_index(drop=True)
    assert pd.DataFrame.equals(data, data_cleaned_json)
    out, _ = capfd.readouterr()
    assert out == "MonkeyPatch Save\n"
