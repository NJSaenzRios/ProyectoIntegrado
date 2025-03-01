from typing import Dict

import requests
from pandas import DataFrame, read_csv, read_json, to_datetime
from io import StringIO

def temp() -> DataFrame:
    """Get the temperature data.
    Returns:
        DataFrame: A dataframe with the temperature data.
    """
    return read_csv("data/temperature.csv")

def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """Get the public holidays for the given year for Brazil.
    Args:
        public_holidays_url (str): URL to the public holidays.
        year (str): The year to get the public holidays for.
    Raises:
        SystemExit: If the request fails.
    Returns:
        DataFrame: A dataframe with the public holidays.
    """
    url = f"{public_holidays_url}/{year}/BR"
    try:
        response = requests.get(url)
        response.raise_for_status()
        holidays = read_json(StringIO(response.text))
        holidays.drop(columns=["types", "counties"], errors="ignore", inplace=True)
        holidays["date"] = to_datetime(holidays["date"])
        return holidays
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """Extract the data from the csv files and load them into the dataframes.
    Args:
        csv_folder (str): The path to the csv's folder.
        csv_table_mapping (Dict[str, str]): The mapping of the csv file names to the
        table names.
        public_holidays_url (str): The url to the public holidays.
    Returns:
        Dict[str, DataFrame]: A dictionary with keys as the table names and values as
        the dataframes.
    """
    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }
   
    dataframes["public_holidays"] = get_public_holidays(public_holidays_url, "2017")
    return dataframes
