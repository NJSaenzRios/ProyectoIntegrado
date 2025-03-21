from typing import Dict
from pandas import DataFrame
from sqlalchemy.engine.base import Engine


def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
        database (Engine): SQLAlchemy engine for database connection
    """

    try:
            
        for table_name, df in data_frames.items():
        
            df.to_sql(table_name, database, if_exists="replace", index=False)
           

    except Exception as e:       
        raise SystemExit(f"Error al cargar los datos en la base de datos: {e}")   
    print("\nCarga de datos")
