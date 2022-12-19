"""Tests for the cleaning module"""
import os
import sys

import pandas as pd
from life_expectancy.cleaning import clean_data, load_data, save_data
from . import OUTPUT_DIR

current_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(source_dir)

def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""
    data = load_data()
    data = clean_data(['pt'], data)
    save_data(data)
    pt_life_expectancy_actual = pd.read_csv(
        OUTPUT_DIR / "pt_life_expectancy.csv"
    )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
