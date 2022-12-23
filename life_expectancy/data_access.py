"""Save and load functions
"""

import pandas as pd

from .constant import FILE_NAME, SAVED_FILE

def save_data(data:pd.DataFrame, save_location:str = SAVED_FILE) -> None:
    """Save the data to file"""
    data.to_csv(save_location, index=False)


def load_data(file_name: str = FILE_NAME, sep='\t') -> pd.DataFrame:
    """Load the data into a pd"""
    return pd.read_csv(file_name, sep=sep)
    