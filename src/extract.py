import os
import requests
import pandas as pd
from src.config import get_csv_to_table_mapping

def get_public_holidays(url: str, year: int):
    """
    Obtiene los días festivos públicos de Brasil desde la API Nager.
    """
    try:
        full_url = f"{url}/{year}/BR"   # URL base + año + país
        print("DEBUG url:", url)
        print("DEBUG year:", year)
        full_url = f"{url}/{year}/BR"
        print("DEBUG full_url:", full_url)
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)
        df = df.drop(columns=[c for c in ["types", "counties"] if c in df.columns])

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        return df

    except requests.exceptions.RequestException as e:
        raise SystemExit(f"API request failed: {e}")


def extract(csv_folder: str, csv_table_mapping: dict, public_holidays_url: str):
    """
    Lee los CSV de la carpeta dada y obtiene los días festivos públicos.

    Args:
        csv_folder (str): Ruta de la carpeta con los CSVs.
        csv_table_mapping (dict): Mapeo {archivo_csv: nombre_tabla}.
        public_holidays_url (str): URL base para API de festivos.

    Returns:
        dict[str, pd.DataFrame]: Diccionario con DataFrames por tabla.
    """
    dataframes = {}

    # Cargar todos los CSV de la carpeta
    for csv_file, table_name in csv_table_mapping.items():
        file_path = os.path.join(csv_folder, csv_file)
        df = pd.read_csv(file_path)
        dataframes[table_name] = df

    # Obtener festivos desde la API (con el orden correcto: url primero, luego año)
    public_holidays = get_public_holidays(public_holidays_url, 2017)
    dataframes["public_holidays"] = public_holidays

    return dataframes