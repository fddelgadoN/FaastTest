"""Test functions to test the data access functions"""
from unittest.mock import Mock

import pytest
import pandas as pd
from life_expectancy.ETLs.json_etl import JsonETL
from life_expectancy.ETLs.csv_etl import CsvETL

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"
EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected_json.csv"


def test_load_data_csv(eu_csv_file : pd.DataFrame) -> None:
    """Test the load data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    json_etl = CsvETL(None)
    data = json_etl.load_data()
    assert pd.DataFrame.equals(eu_csv_file, data)

def test_load_data_json(eu_json_file : pd.DataFrame) -> None:
    """Test the load data function

    Args:
        eu_json_file (Fixture): Fixture that loads the json file
    """
    json_etl = JsonETL(None)
    data = json_etl.load_data()
    assert pd.DataFrame.equals(eu_json_file, data)

def test_save_data(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the save data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    mock_print = Mock(return_value='MonkeyPatch save')
    monkeypatch.setattr("life_expectancy.tests.test_data_access.JsonETL.save_data",
                        lambda _ : print(mock_print()))
    dummy_data = pd.DataFrame()
    JsonETL.save_data(dummy_data)
    mock_print.assert_called()
