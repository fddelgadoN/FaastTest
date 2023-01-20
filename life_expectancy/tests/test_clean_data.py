"""Test cleaning functions"""
from unittest.mock import Mock

import pandas as pd
import pytest

from life_expectancy import data_access
from life_expectancy.cleaning import main

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"


def test_main(monkeypatch : pytest.MonkeyPatch, data_cleaned: pd.DataFrame) -> None:
    """Test the main function that loads, cleans and saves the data, monkeypatching the data access
    functions so it does not alter data. Checking aswell if save_data is called

    Args:
        monkeypatch (Monkeypatch): MonkeyPatch object
        data_cleaned (Fixture): Data fixture with cleaned data
    """
    mock_print = Mock(return_value='MonkeyPatch save')
    monkeypatch.setattr( "life_expectancy.cleaning.save_data", lambda _ : print(mock_print()))
    monkeypatch.setattr( "life_expectancy.cleaning.load_data", lambda  :
                data_access.load_data(EU_FILE_NAME, ","))
    data = main().reset_index(drop=True)
    assert pd.DataFrame.equals(data, data_cleaned)
    mock_print.assert_called()
