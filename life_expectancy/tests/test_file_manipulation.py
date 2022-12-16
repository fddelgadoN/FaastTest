import pytest 

import pandas as pd

from life_expectancy.loaders import save_data, load_data
from life_expectancy.cleaning import clean_data


DATA_LOCATION = "life_expectancy/data/eu_life_expectancy_raw.tsv"
SAVE_LOCATION = "life_expectancy/tests/fixtures/"
FILE_NAME = "eu_life_expectancy_expected.csv"
CLEANED_FILE_NAME = "pt_life_expectancy_expected.csv"

@pytest.fixture
def data_fixture():
    data = load_data(DATA_LOCATION)
    data = data.iloc[:100]
    return data



def test_load_data(data_fixture):
    """Test the save data

    Args:
        data_fixture (pytest.fixture): loads the original data and samples it
    """
    data = pd.read_csv(DATA_LOCATION, sep='\t')[:100]
    assert pd.DataFrame.equals(data, data_fixture)
