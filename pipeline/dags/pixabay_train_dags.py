import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append(os.getcwd())
from pipeline.utils.constants import AIRFLOW_DEFAULT_ARGS
from pipeline.tasks.pixabay_tasks import PixabayTask

with DAG(
        dag_id="pixabay_super_resolution",
        start_date=datetime.today().replace(minute=0),
        default_args=AIRFLOW_DEFAULT_ARGS,
        schedule_interval="*/15 * * * *",  # every 15 minutes
) as pixabay_train_dag:
    task = PixabayTask(date_time=datetime.today(), limit=5)

    extract_pixabay_task = PythonOperator(
        task_id="pixabay_extract_task",
        python_callable=task.extract_source_image,
    )
    train_pixabay_task = PythonOperator(
        task_id="pixabay_train_task",
        python_callable=task.train_original_image,
    )
    upload_pixabay_task = PythonOperator(
        task_id="pixabay_upload_task",
        python_callable=task.upload_sr_image,
    )

    extract_pixabay_task >> train_pixabay_task >> upload_pixabay_task
