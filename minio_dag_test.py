"""
Example DAG demonstrating the usage of the TaskFlow API to execute Python functions natively and within a
virtual environment.
"""
import os
import logging
import time
import datetime
from minio import Minio
from minio.error import S3Error

from airflow import DAG
from airflow.decorators import task

log = logging.getLogger(__name__)

def minio_add_bucket(bucket_name, minio_service = 'minio-service.default.svc.cluster.local',
                            minio_port='9000',
                            username = 'testkey',
                            password = 'secretkey', **kwargs):

        minio_endpoin = ':'.join((minio_service, minio_port))              

        print('Connecting to %s with user %s and password %s.' %(minio_endpoint, username, password))

        minio_client = Minio(minio_endpoint, 
                                access_key = username,
                                secret_key = password,
                                secure = False)
        try:
            if (not minio_client.bucket_exists(bucket_name)):
                minio_client.make_bucket(bucket_name)
            else:
                print('Bucket \'%s\' already exists' %(bucket_name))
        except S3Error as exc:
            print("Error occurred during bucket query/creation:", exc)


        path = "/mnt/c/Users/EoinCarley/Desktop/musicapp.songs/mp3files/"
        filenames = os.listdir(path)
        print(filenames)
        #for file in filenames:
        #    minio_client.fput_object(
        #        bucket_name, file, ''.join((path, file)))
        #return None

        

with DAG(
    dag_id='MusicApp-DAG',
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
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
    def minio_add_bucket(bucket_name, minio_service = 'minio-service.default.svc.cluster.local',
                            minio_port = '9000',
                            username = 'testkey',
                            password = 'secretkey', **kwargs):

        minio_endpoint = ':'.join((minio_service, minio_port))              

        print('Connecting to %s with user %s and password %s.' %(minio_endpoint, username, password))

        minio_client = Minio(minio_endpoint, 
                                access_key = username,
                                secret_key = password,
                                secure = False)
        try:
            if (not minio_client.bucket_exists(bucket_name)):
                minio_client.make_bucket(bucket_name)
            else:
                print('Bucket \'%s\' already exists' %(bucket_name))
        except S3Error as exc:
            print("Error occurred during bucket query/creation:", exc)
        
        #--------------------------------------------------------#
        #    Define bucket, Minio endpoint. Setup Minio client
        #
        # Note here I'll need to mount a volume to the localhost. 
        # See https://www.aylakhan.tech/?p=655 for potential solution:
        # 

        # See values.yaml for this volume mount definition.
        try:
            path = "/mnt/miniovolume"
            filenames = os.listdir(path)
            print(filenames)
        except:
            print('Cannot list filenames in %s' %(path))
        #for file in filenames:
        #    minio_client.fput_object(
        #        bucket_name, file, ''.join((path, file)))
        #return None

    task1 = minio_add_bucket('songs')

task1 >> task2 >> task3
