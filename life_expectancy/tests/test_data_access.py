"""Test functions to test the data access functions"""
import pandas as pd
from life_expectancy.data_access import CSVLoader

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"


def test_load_data(eu_csv_file : pd.DataFrame) -> None:
    """Test the load data function

    Args:
        eu_csv_file (Fixture): Fixture that loads the tsv file
    """
    loader = CSVLoader(None)
    data = loader.load_data()
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
