import logging
import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append(os.getcwd())
log = logging.getLogger(__name__)

with DAG(
    dag_id="adobe_image_training",
    start_date=datetime.today()+timedelta(days=-1),
    schedule_interval="@once"
) as adoboe_train_dag:
    from isr.utils.pipeline import Pipeline
    pipeline = Pipeline("adobe")

    extract_adobe_task = PythonOperator(
        task_id="adobe_extract_task",
        python_callable=pipeline.extract_source_image,
    )
    train_adobe_task = PythonOperator(
        task_id="adobe_train_task",
        python_callable=pipeline.train_image,
    )
    upload_adobe_task = PythonOperator(
        task_id="upload_adobe_task",
        python_callable=pipeline.upload_trained_image,
    )

    extract_adobe_task >> train_adobe_task >> upload_adobe_task
