import pytest

import pandas as pd

from life_expectancy import data_access
from life_expectancy.cleaning import clean_data


DATA_LOCATION = "life_expectancy/data/eu_life_expectancy_raw.tsv"
SAVE_LOCATION = "life_expectancy/tests/fixtures/"
DATA_FOLDER = "life_expectancy/data/"
EU_FILE_NAME = DATA_FOLDER+"eu_life_expectancy_expected.csv"
PT_FILE_NAME =DATA_FOLDER+"pt_life_expectancy_expected.csv"

@pytest.fixture
def data_fixture():
    data = data_access.load_data(DATA_LOCATION)
    data = data.iloc[:100]
    data_access.save_data(data, EU_FILE_NAME)
    dataframe = clean_data(argv = "pt", data=data)
    data_access.save_data(dataframe, PT_FILE_NAME)

    return data



def test_load_data(data_fixture):
    """Test the save data

    Args:
        data_fixture (pytest.fixture): loads the original data and samples it
    """
    data = pd.read_csv(DATA_LOCATION, sep='\t')[:100]
    assert pd.DataFrame.equals(data, data_fixture)

def _monkey_save():
    print("MonkeyPatch save")
    return pd.read_csv("life_expectancy/data/pt_life_expectancy_expected_fixture.csv", sep='\t')


def test_clean_data(data_fixture, monkeypatch):
    monkeypatch.setattr(data_access, "save_data", _monkey_save)
    data = clean_data('pt', data_fixture)
    assert pd.DataFrame.equals(data, data_access.save_data)

