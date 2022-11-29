import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append(os.getcwd())
from pipeline.utils.constants import AIRFLOW_DEFAULT_ARGS
from pipeline.tasks.pexels_tasks import PexelsTask

with DAG(
        dag_id="pexels_super_resolution",
        start_date=datetime.today().replace(minute=0),
        default_args=AIRFLOW_DEFAULT_ARGS,
        schedule_interval="*/10 * * * *",  # every 10 minutes
) as pexels_train_dag:
    task = PexelsTask(date_time=datetime.today(), limit=50)

    extract_pexels_task = PythonOperator(
        task_id="pexels_extract_task",
        python_callable=task.extract_source_image,
    )
    train_pexels_task = PythonOperator(
        task_id="pexels_train_task",
        python_callable=task.train_original_image,
    )
    upload_pexels_task = PythonOperator(
        task_id="pexels_upload_task",
        python_callable=task.upload_sr_image,
    )

    extract_pexels_task >> train_pexels_task >> upload_pexels_task
