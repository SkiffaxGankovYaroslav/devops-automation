#import json
#import time #for sleep
import logging
import boto3
#import datetime #for date-now
from datetime import datetime
import os #maybe it needed for uploading file
from botocore.exceptions import ClientError

#setting variables
name_bucket="bucket-from-lambda-skiff"
name_file_clear="file1.txt"
name_file="/tmp/"+name_file_clear

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # response = s3.list_buckets()
    # print('Existing buckets:')
    # for bucket in response['Buckets']:
    #     print(f'  {bucket["Name"]}')
    create_bucket(name_bucket)
    s3.download_file(name_bucket, name_file_clear, name_file)

#   print(f"try count: {i}") #for debug
    #creating file with now-data
    with open(name_file, "a+") as file: #mode "a" means that text will appended to file
        file.write(str(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))+"\n")
    #upload created file to the bucket
    upload_file(name_file, name_bucket, name_file_clear)
    #time.sleep(sleep_time)

#standart function from AWS quickstart documentation
def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#standart function from AWS quickstart documentation
def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
