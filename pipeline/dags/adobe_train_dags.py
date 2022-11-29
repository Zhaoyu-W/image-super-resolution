import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append(os.getcwd())
from pipeline.utils.constants import AIRFLOW_DEFAULT_ARGS
from pipeline.tasks.adobe_tasks import AdobeTask

with DAG(
        dag_id="adobe_super_resolution",
        start_date=datetime.today().replace(minute=0),
        default_args=AIRFLOW_DEFAULT_ARGS,
        schedule_interval="*/1 * * * *",  # every minute
) as adobe_train_dag:
    task = AdobeTask(date_time=datetime.today(), limit=50)

    extract_adobe_task = PythonOperator(
        task_id="adobe_extract_task",
        python_callable=task.extract_source_image,
    )
    train_adobe_task = PythonOperator(
        task_id="adobe_train_task",
        python_callable=task.train_original_image,
    )
    upload_adobe_task = PythonOperator(
        task_id="adobe_upload_task",
        python_callable=task.upload_sr_image,
    )

    extract_adobe_task >> train_adobe_task >> upload_adobe_task
