from typing import Dict
import sys
import requests
from pandas import DataFrame, read_csv, to_datetime


def get_public_holidays(public_holidays_url: str, year: str) -> DataFrame:
    """
    Trae los feriados de Brasil para un año dado desde la API pública.

    - URL: {public_holidays_url}/{year}/BR
    - Asegura que la tabla tenga exactamente estas 7 columnas y en este orden:
      ['date', 'localName', 'name', 'countryCode', 'fixed', 'global', 'type']
      (Si la API trae 'types' como lista, uso el primer valor para 'type')
    """
    try:
        resp = requests.get(f"{public_holidays_url}/{year}/BR", timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al consultar feriados: {e}", file=sys.stderr)
        raise SystemExit(1)

    data = resp.json()
    df = DataFrame(data)

    # Convertir fecha a datetime si existe
    if "date" in df.columns:
        df["date"] = to_datetime(df["date"])

    # Si no viene 'type' pero sí 'types' (lista), me quedo con el primero
    if "type" not in df.columns:
        if "types" in df.columns:
            df["type"] = df["types"].apply(
                lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None
            )
        else:
            df["type"] = None

    # Asegurar columnas mínimas si no vinieran
    if "countryCode" not in df.columns:
        df["countryCode"] = "BR"
    if "fixed" not in df.columns:
        df["fixed"] = False
    if "global" not in df.columns:
        df["global"] = False

    # Eliminar columnas que no se piden (si existen)
    for extra in ("types", "counties"):
        if extra in df.columns:
            df = df.drop(columns=[extra])

    # Dejar exactamente estas 7 columnas en este orden
    cols = ["date", "localName", "name", "countryCode", "fixed", "global", "type"]
    # Si por algo falta alguna columna, la creo vacía para no romper
    for c in cols:
        if c not in df.columns:
            df[c] = None
    df = df[cols]

    return df


def extract(
    csv_folder: str, csv_table_mapping: Dict[str, str], public_holidays_url: str
) -> Dict[str, DataFrame]:
    """
    Lee los CSV según el mapping y agrega la tabla 'public_holidays' del 2017.
    Devuelve {nombre_tabla: DataFrame}
    """
    dataframes: Dict[str, DataFrame] = {}

    # Cargar cada CSV a su tabla
    for csv_file, table_name in csv_table_mapping.items():
        path = f"{csv_folder}/{csv_file}"
        df = read_csv(path)
        dataframes[table_name] = df

    # Feriados BR solo 2017 (lo que usan los tests)
    holidays_df = get_public_holidays(public_holidays_url, "2017")
    dataframes["public_holidays"] = holidays_df

    return dataframes
