import sys
import os

sys.path.insert(0, "/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from pipeline.build_index import run_build_index

with DAG(
    dag_id="rag_ingest_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["rag"],
) as dag:

    ingest_task = PythonOperator(
        task_id="build_index",
        python_callable=run_build_index,
        provide_context=True,
    )
