import os
import logging
import time
import datetime
from minio import Minio
from minio.error import S3Error


minio_port = '9000'
minio_service = 'localhost'
minio_endpoint = ':'.join((minio_service, minio_port))
username = 'testkey'
password = 'secretkey'
bucket_name = 'songs'

print('Attempting to connect to %s with user %s and password %s.' %(minio_endpoint, username, password))

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
for file in filenames:
    minio_client.fput_object(
        bucket_name, file, ''.join((path, file)))