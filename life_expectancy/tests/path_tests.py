"""Module with attr for path constants"""
from dataclasses import dataclass, field

@dataclass
class FilePathsTest:
    """Class with path for the files used in testing"""
    output_dir: str
    data_location_csv: str = field(init=False)
    data_location_json: str = field(init=False)
    pt_file_name_csv: str = field(init=False)
    pt_file_name_json:  str = field(init=False)

    def __post_init__(self):
        self.data_location_csv = self.output_dir/"eu_life_expectancy_raw.tsv"
        self.data_location_json = self.output_dir/"eurostat_life_expect.json"
        self.pt_file_name_csv = self.output_dir/"pt_life_expectancy_expected.csv"
        self.pt_file_name_json = self.output_dir/"pt_life_expectancy_expected_json.csv"
