"""Constant module"""
from dataclasses import dataclass, field

@dataclass
class FILEPATHS():
    """Dataclass with all the files path"""
    data_folder: str = field(default="life_expectancy/data/")
    saved_file: str = field(init=False)
    csv_file_name: str = field(init=False)
    json_file_name: str = field(init=False)

    def __post_init__(self):
        self.saved_file = self.data_folder+"pt_life_expectancy.csv"
        self.csv_file_name = self.data_folder+"eu_life_expectancy_raw.tsv"
        self.json_file_name = self.data_folder+"eurostat_life_expect.json"
