from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys

sys.path.append("/opt/airflow")

from src.transform.clean_silver_duckdb import transform_bronze_to_silver_duckdb

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'bronze_to_silver_duckdb',
    default_args=default_args,
    description='Transforma datos de Bronze a Silver con DuckDB hacia MinIO',
    schedule_interval='@daily',
    catchup=False,
    tags=['silver', 'duckdb', 'transformation'],
) as dag:

    clean_silver = PythonOperator(
        task_id='transform_bronze_to_silver',
        python_callable=transform_bronze_to_silver_duckdb,
        op_kwargs={'dataset_folder': 'football'}
    )

    clean_silver
