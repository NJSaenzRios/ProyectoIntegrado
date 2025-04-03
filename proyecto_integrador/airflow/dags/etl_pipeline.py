import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sqlite3
import pandas as pd

# Ruta de la base de datos en el contenedor
DB_PATH = "/opt/airflow/olist.db"

# Función de extracción
# Función de extracción con rutas corregidas
def extract():
    csv_path = "/dataset/olist_orders_dataset.csv"  # Asegúrate de usar la ruta correcta
    df = pd.read_csv(csv_path)
    df.to_csv("/opt/airflow/dags/extracted_orders.csv", index=False)
    print(f" Datos extraídos de {csv_path} y guardados en CSV")


# Función de transformación
# Función de transformación con rutas corregidas
def transform():
    extracted_path = "/opt/airflow/dags/extracted_orders.csv"
    transformed_path = "/opt/airflow/dags/transformed_orders.csv"

    # Verifica que el archivo existe antes de leerlo
    if not os.path.exists(extracted_path):
        print(f"ERROR: No se encontró el archivo {extracted_path}.")
        return
    
    df = pd.read_csv(extracted_path)
    
    # Aplica una transformación simple para probar
    df["new_column"] = "processed"  
    
    df.to_csv(transformed_path, index=False)

    print(f" Transformación completada. Archivo guardado en {transformed_path}")

def load():
    df = pd.read_csv("/opt/airflow/dags/transformed_orders.csv")
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("orders_transformed", conn, if_exists="replace", index=False)
    conn.close()
    print("Datos cargados en la base de datos")



default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 31),
    "catchup": False,
}

# Creación del DAG
with DAG(
    dag_id="etl_pipeline",
    default_args=default_args,
    schedule="@daily",  # Se ejecuta diariamente
) as dag:

    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform
    )

    task_load = PythonOperator(
        task_id="load_data",
        python_callable=load
    )

    # Definimos la secuencia de ejecución
    task_extract >> task_transform >> task_load
