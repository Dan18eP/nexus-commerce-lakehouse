from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.append("/opt/airflow")

from src.extract.kaggle_downloader import download_and_upload_kaggle_dataset

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'kaggle_bronze_ingest',
    default_args=default_args,
    description='Descarga datos crudos desde Kaggle y los almacena en MinIO Bronze',
    schedule_interval='@daily',
    catchup=False,
    tags=['bronze', 'kaggle', 'ingestion'],
) as dag:

    def ingest_task():
        # Dataset de ejemplo por defecto o configurable
        dataset = os.getenv("KAGGLE_DATASET", "davidcariboo/player-scores")
        download_and_upload_kaggle_dataset(dataset_identifier=dataset, target_bronze_folder="football")

    ingest_bronze = PythonOperator(
        task_id='ingest_bronze_from_kaggle',
        python_callable=ingest_task
    )

    ingest_bronze
