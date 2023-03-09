"""Test functions to test the data access functions"""
from unittest.mock import Mock

import pytest
from life_expectancy import data_access
import pandas as pd

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"


def test_load_data(eu_csv_file : pd.DataFrame) -> None:
    """Test the load data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    data = data_access.load_data()
    assert pd.DataFrame.equals(eu_csv_file, data)

def test_save_data(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the save data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    mock_print = Mock(return_value='MonkeyPatch save')
    monkeypatch.setattr( "life_expectancy.data_access.save_data", lambda _ : print(mock_print()))
    dummy_data = pd.DataFrame()
    data_access.save_data(dummy_data)
    mock_print.assert_called()
