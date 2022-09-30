
import os
import logging
import time
import datetime


from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)


with DAG(
    dag_id='Xcom-test',
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:
  
    #--------------------------------------------------------#
    #
    #       Add bucket via the Minio client object.
    #
    @task(task_id="Task1")
    def taskone(**kwargs):             

        print('Doing task 1')
        a = [1,2,3,4]
        
        kwargs['ti'].xcom_push(key='someobject', value=a)
        
        return None

    task1 = taskone()

    #--------------------------------------------------------#
    #    Define bucket, Minio endpoint. Setup Minio client
    #
    @task(task_id="Task2")
    def tasktwo(**kwargs):
        print('Doing Task2')

        ti = kwargs['ti']
        name = ti.xcom_pull(task_ids='Task1', key='someobject')
        print(name)
        
        return None


    task2 = tasktwo()

task1 >> task2 

if __name__ == "__main__":
    from airflow.utils.state import State

    dag.clear()
    dag.run()