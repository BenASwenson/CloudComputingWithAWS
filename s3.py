import logging
import boto3
from botocore.exceptions import ClientError
import os


# create bucket

def create_bucket(bucket_name, region=None):

    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


create_bucket("eng110-bens", "eu-west-1")


# upload data

def upload_file(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return True


upload_file("test.txt", "eng110-bens")


# download data

def download_file():

    s3 = boto3.client('s3')
    s3.download_file('eng110-bens', "screenshot.png", "screenshot2.png")


download_file()


# update and replace

def update_replace(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)

    return True


update_replace("test.txt", "eng110-bens", "test.txt")


# deleting data


def delete_file():

    s3 = boto3.resource('s3')
    obj = s3.Object("eng110-bens", "test.txt")
    obj.delete()


delete_file()



