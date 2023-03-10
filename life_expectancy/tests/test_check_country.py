"""Test for the check_country_exists function in BaseEtl"""
from life_expectancy.etls.json_etl import JsonETL

EU_FILE_NAME = "life_expectancy/data/eu_life_expectancy_expected.csv"

def test_check_country():
    """Test check country function"""
    cleaner = JsonETL(EU_FILE_NAME)
    country = 'WRONG'
    assert not cleaner.check_country_exists(country)
    country = 'PT'
    assert cleaner.check_country_exists(country)
    