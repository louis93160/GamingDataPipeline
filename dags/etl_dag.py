from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Ajout du chemin du répertoire `scripts` au `PYTHONPATH`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from pipeline_etl import fetch_and_store_top_games 

# Configuration du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_top_games',
    default_args=default_args,
    description='Fetch and store top 15 games based on reviews',
    schedule_interval=timedelta(days=1),
    catchup=False, 
)

# Tâche Python
fetch_top_games_task = PythonOperator(
    task_id='fetch_top_games',
    python_callable=fetch_and_store_top_games,
    dag=dag,
)

fetch_top_games_task
