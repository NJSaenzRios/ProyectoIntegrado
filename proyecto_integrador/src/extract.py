import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict
import requests
import pandas as pd
from pandas import DataFrame, read_csv, read_json, to_datetime
from src.config import PUBLIC_HOLIDAYS_URL

def temp() -> DataFrame:
    """Get the temperature data.
    Returns:
        DataFrame: A dataframe with the temperature data.
    """
    return read_csv("data/temperature.csv")

def get_public_holidays(public_holidays_url: str = PUBLIC_HOLIDAYS_URL, year: str = "2024", country: str = "BR") -> pd.DataFrame:
    """Get the public holidays for the given year for Brazil."""
    url = f"{public_holidays_url}/{year}/BR"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud falla
        data = response.json()
        
        df = pd.DataFrame(data)  # Almacena la consulta en un DataFrame
        df.drop(columns=["types", "counties"], inplace=True, errors='ignore')
        df["date"] = pd.to_datetime(df["date"])
        
        return df
    except requests.RequestException as e:
        raise SystemExit(f"Error en la solicitud: {e}")



def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str = PUBLIC_HOLIDAYS_URL,
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

    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes
