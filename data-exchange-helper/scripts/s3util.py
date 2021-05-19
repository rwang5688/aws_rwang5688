import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_s3_client():
    region_name = ''
    if 'TARGET_REGION' in os.environ:
        region_name = os.environ['TARGET_REGION']
    print('get_s3_client: region_name=%s' % region_name)

    session = boto3.Session(profile_name=None)
    s3 = session.client('s3',
        region_name=region_name)
    return s3


def list_buckets():
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Print bucket names
    print('\nBuckets:')
    if 'Buckets' in response:
        for bucket in response['Buckets']:
            print('Name: %s' % bucket["Name"])


def get_bucket(bucket_name):
    # Retrieve the list of existing buckets
    s3 = get_s3_client()
    response = s3.list_buckets()

    # Find the bucket by name
    result = None
    for bucket in response['Buckets']:
        if bucket["Name"] == bucket_name:
            result = bucket
            break

    return result


def file_exists(bucket_name, object_name):
    s3 = get_s3_client()
    try:
        head_object = s3.head_object(Bucket=bucket_name, Key=object_name)
        print("s3util.file_exists: object_name=%s, head_object=%s" % (object_name, head_object))
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("s3util.file_exists: %s file object not found" % object_name)
            return False
        else:
            logging.error("s3util.file_exists: unexpected error:")
            logging.exception(e)
            return False
    else:
        return True


def get_file_blob(bucket_name, object_name):
    s3 = get_s3_client()
    result = None
    try:
        file_object = s3.get_object(Bucket=bucket_name, Key=object_name)
        print('s3util.get_file_blob: object_name=%s, file_object=%s' % (object_name, file_object))
        if file_object is None:
            print('s3util.get_file_blob: Failed to get file object %s' % object_name)
            return None
        result = file_object['Body'].read()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("s3util.get_file_blob: %s file object not found" % object_name)
            return None
        else:
            logging.error("s3util.get_file_blob: unexpected error:")
            logging.exception(e)
            return None
    else:
        return result


def list_files(bucket_name):
    # Retrieve the list of existing files
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Print bucket name and object keys
    print('\nBucket: %s' % response["Name"])
    print('Contents:')
    if 'Contents' in response:
        for bucketFile in response['Contents']:
            print('Key: %s' % bucketFile["Key"])


def upload_file(file_name, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_name

    s3 = get_s3_client()
    try:
        response = s3.upload_file(file_name, bucket_name, object_name)
        print('s3util.upload_file: file_name=%s, response=%s' % (file_name, response))
    except ClientError as e:
        logging.error("s3util.upload_file: unexpected error:")
        logging.error(e)
        return False
    else:
        return True


def download_file(bucket_name, object_name, file_name=None):
    if file_name is None:
        file_name = object_name

    s3 = get_s3_client()
    try:
        response = s3.download_file(bucket_name, object_name, file_name)
        print('s3util.download_file: object_name=%s, response=%s' % (object_name, response))
    except ClientError as e:
        logging.error("s3util.download_file: unexpected error:")
        logging.error(e)
        return False
    else:
        return True

