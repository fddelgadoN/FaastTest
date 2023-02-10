"""Test cleaning functions"""
from unittest.mock import Mock

import pandas as pd
import pytest

from life_expectancy.main import main
from life_expectancy.file_type import FileExtension
from life_expectancy.cleaning import Cleaner

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"
EU_FILE_NAME_JSON = "life_expectancy/data/eu_life_expectancy_expected_json.csv"

def test_main_csv(monkeypatch : pytest.MonkeyPatch, data_cleaned_csv: pd.DataFrame) -> None:
    """Test the main function that loads, cleans and saves the data, monkeypatching the data access
    functions so it does not alter data. Checking aswell if save_data is called

    Args:
        monkeypatch (Monkeypatch): MonkeyPatch object
        data_cleaned_csv (Fixture): Data fixture with cleaned data
    """
    mock_print = Mock(return_value='MonkeyPatch save')
    monkeypatch.setattr("life_expectancy.main.save_data", lambda _ : print(mock_print()))
    monkeypatch.setattr("life_expectancy.main.CSVCleaner.load_data", lambda _ :
                pd.read_csv(EU_FILE_NAME, ","))
    data = main().reset_index(drop=True)
    assert pd.DataFrame.equals(data, data_cleaned_csv)
    mock_print.assert_called()


def test_main_json(monkeypatch : pytest.MonkeyPatch, data_cleaned_json: pd.DataFrame) -> None:
    """Test the main function that loads, cleans and saves the data, monkeypatching the data access
    functions so it does not alter data. Checking aswell if save_data is called

    Args:
        monkeypatch (Monkeypatch): MonkeyPatch object
        data_cleaned_json (Fixture): Data fixture with cleaned data
    """

    mock_print = Mock(return_value='MonkeyPatch save')
    monkeypatch.setattr("life_expectancy.main.save_data", lambda _ : print(mock_print()))
    monkeypatch.setattr("life_expectancy.main.JSONCleaner.load_data", lambda _:
                pd.read_csv(EU_FILE_NAME_JSON, ","))
    data = main(file_type = FileExtension.JSON).reset_index(drop=True)
    assert pd.DataFrame.equals(data, data_cleaned_json)
    mock_print.assert_called()


def test_check_country():
    """Test check country function"""
    cleaner = Cleaner(EU_FILE_NAME)
    country = 'WRONG'
    assert not cleaner.check_country_exists(country)
    country = 'PT'
    assert cleaner.check_country_exists(country)
    