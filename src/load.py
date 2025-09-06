from typing import Dict

from pandas import DataFrame
from sqlalchemy.engine.base import Engine


def load(data_frames: Dict[str, DataFrame], database: Engine):
    """
    Carga los dataframes dentro de la base de datos sqlite.

    Args:
        data_frames (Dict[str, DataFrame]): diccionario con el nombre de la tabla
        como clave y el dataframe como valor.
        database (Engine): conexión a la base de datos.
    """
    import sqlite3  # uso sqlite3 directo porque pandas lo maneja bien así
    
    # La ruta de la base de datos se puede sacar del engine
    database_url = str(database.url)
    
    # Si es una base SQLite de archivo
    if "sqlite:///" in database_url:
        db_path = database_url.replace("sqlite:///", "")
        
        # Me conecto directo con sqlite3 y voy guardando cada dataframe
        with sqlite3.connect(db_path) as conn:
            for table_name, df in data_frames.items():
                df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)
    else:
        # Si no es SQLite, entonces uso el engine normal
        for table_name, df in data_frames.items():
            df.to_sql(name=table_name, con=database, if_exists="replace", index=False)