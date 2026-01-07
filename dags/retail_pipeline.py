from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Crucial Step: We add our scripts folder to the system path so Airflow can 'see' them
sys.path.append(os.path.dirname(__file__))

# Import the functions we just wrote in the other files
from scripts.generate_data import generate_daily_sales
from scripts.load_to_db import load_data

# Paths for Codespaces (Absolute paths prevent "File Not Found" errors)
DATA_PATH = '/workspaces/retail-etl-pipeline/data/sales_data.csv'
DB_PATH = '/workspaces/retail-etl-pipeline/data/retail_wh.duckdb'

default_args = {
    'owner': 'vivek',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='daily_retail_ingest',
    default_args=default_args,
    description='A simulated Retail ETL pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False, # Don't run for past dates, only new ones
    tags=['retail', 'project_1']
) as dag:

    # Task 1: Create the Fake Data
    t1_extract = PythonOperator(
        task_id='extract_sales_data',
        python_callable=generate_daily_sales,
        op_kwargs={'file_path': DATA_PATH}
    )

    # Task 2: Load it into the Database
    t2_load = PythonOperator(
        task_id='load_to_duckdb',
        python_callable=load_data,
        op_kwargs={'csv_path': DATA_PATH, 'db_path': DB_PATH}
    )

    # The "Dependency" -> Run T1, then T2
    t1_extract >> t2_load