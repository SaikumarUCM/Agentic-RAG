

import sys
sys.path.insert(0, '/opt/airflow')

from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime

from pipeline.build_index import run_build_index

with DAG(
    dag_id="rag_ingest_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["rag"],
) as dag:

    ingest_task = PythonOperator(
        task_id="build_index",
        python_callable=run_build_index,
    )
