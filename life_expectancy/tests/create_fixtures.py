from cleaning import load_data, save_data, clean_data
from constant import DATA_LOCATION

def main():
    data = load_data()
    data = data.iloc[:100]
    save_data(data, DATA_LOCATION+"eu_lift_expectancy_expected_fixture.csv")
    dataframe = clean_data(argv = "pt", data=data)
    save_data(dataframe, DATA_LOCATION+"pt_lift_expectancy_expected_fixture.csv")


if __name__ == "__main__":
    main()