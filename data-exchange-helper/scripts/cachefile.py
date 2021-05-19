import os
import s3util


def get_task_attribute_value(task, task_attribute_name):
    task_attribute_value = ''
    if task_attribute_name in task:
        task_attribute_value = task[task_attribute_name]
    else:
        print('get_task_attribute_value: Task attribute %s is not defined.' % task_attribute_name)

    return task_attribute_value


def file_exists(bucket_name, task, cache_name, cache_id_attribute_name, cache_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('file_exists: Bucket %s does not exist.' % bucket_name)
        return None

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return None

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return None

    # get {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    return s3util.file_exists(bucket_name, cache_file_object_name)


def get_cache_file_blob(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('get_cache_file_blob: Bucket %s does not exist.' % bucket_name)
        return None

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return None

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return None

    # get {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    cache_file_blob = s3util.get_file_blob(bucket_name, cache_file_object_name)
    if cache_file_blob is None:
        print('get_cache_file_blob: Failed to get file blob %s' % cache_file_object_name)
        return None

    return cache_file_blob


def upload_cache_file(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name, \
    local_cache_dir=None):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('upload_cache_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return ''

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return ''

    # upload {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    upload_file_name = cache_file_name
    if local_cache_dir is not None:
        upload_file_name = os.path.join(local_cache_dir, cache_file_name)
    if not os.path.exists(upload_file_name):
        print('upload_cache_file: File %s does not exist' % upload_file_name)
        return ''

    success = s3util.upload_file(upload_file_name, bucket_name, cache_file_object_name)
    if not success:
        print('upload_cache_file: Failed to upload file %s.' % cache_file_name)
        return ''

    # success
    return upload_file_name


def download_cache_file(bucket_name, task, \
    cache_name, cache_id_attribute_name, cache_file_attribute_name, \
    local_cache_dir=None):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('download_cache_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get cache_id, cache_file_name
    cache_id = get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return ''

    cache_file_name = get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return ''

    # download {cache_name}/{cache_id}/{cache_file_name}
    cache_file_object_name = cache_name + "/" + cache_id + "/" + cache_file_name
    download_file_name = cache_file_name
    if local_cache_dir is not None:
        download_file_name = os.path.join(local_cache_dir, cache_file_name)
    success = s3util.download_file(bucket_name, cache_file_object_name, download_file_name)
    if not success:
        print('download_cache_file: Failed to download file %s.' % cache_file_name)
        return ''

    # success
    return download_file_name

