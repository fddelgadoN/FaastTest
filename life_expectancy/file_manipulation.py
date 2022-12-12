"""Save and load functions
"""

import pandas as pd
# pylint: disable=import-error
from constant import DATA_LOCATION, FILE_NAME, SAVED_FILE
# pylint: enable=import-error

def save_data(data:pd.DataFrame, save_location:str = DATA_LOCATION+SAVED_FILE) -> None:
    """Save the data to file"""
    data.to_csv(save_location, index=False)


def load_data(file_name: str = DATA_LOCATION+FILE_NAME) -> pd.DataFrame:
    """Load the data into a pd"""
    return pd.read_csv(file_name, sep='\t')
