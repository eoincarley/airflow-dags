"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
import logging
import time
import pendulum
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
  
    #--------------------------------------------------------#
    #    Define bucket, Minio endpoint. Setup Minio client
    #
    @task(task_id='add_info_to_db')
    def add_info_to_db():
        print('Added song information to database.')

    task3 = add_info_to_db()

    #--------------------------------------------------------#
    #    Define bucket, Minio endpoint. Setup Minio client
    #
    @task(task_id='add_songs_to_bucket')
    def add_songs_to_bucket():
        print('Adding songs to Minio bucket')

    task2 = add_songs_to_bucket()

    #--------------------------------------------------------#
    #    Define bucket, Minio endpoint. Setup Minio client
    #
    @task(task_id="minio_add_bucket")
    def minio_add_bucket(bucket_name, **kwargs):
       
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

task1 >> task2 >> task3