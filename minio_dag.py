"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
import logging
import time
#from minio import Minio
#from minio.error import S3Error

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

with DAG(
    dag_id='Minio-DAG',
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:
  
    @task(task_id='justprint')
    def printtask():
        print('Not doing anything in particular')

    task2 = printtask()

    @task(task_id="print_the_context")
    def minio_add_bucket(bucket_name, **kwargs):
        #--------------------------------------------------------#
        #    Define bucket, Minio endpoint. Setup Minio client
        #
        minio_port = ':9000'
        minio_service = 'minio-service'
        minio_endpoint = ''.join((minio_service, minio_port))
        username = 'testkey'
        password = 'secretkey'

        print('Attempting to connect to %s with user %s and password %s.' %(minio_endpoint, username, password))

        '''
        minio_client = get_minio_client('testkey', 'secretkey', 
                                        minio_endpoint=minio_endpoint)
        try:
            if (not minio_client.bucket_exists(bucket_name)):
                minio_client.make_bucket(bucket_name)
            else:
                print('Bucket \'%s\' already exists' %(bucket_name))
        except S3Error as exc:
            print("Error occurred during bucket query/creation:", exc)
        '''
        return None

    task1 = minio_add_bucket('songs')

task1 >> task2