import s3util


def get_task_attribute_value(task, task_attribute_name):
    task_attribute_value = ''
    if task_attribute_name in task:
        task_attribute_value = task[task_attribute_name]
    else:
        print('get_task_attribute_value: Task attribute %s is not defined.' % task_attribute_name)

    return task_attribute_value


def get_task_file_blob(bucket_name, task, task_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('get_task_file_blob: Bucket %s does not exist.' % bucket_name)
        return None

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return None

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return None

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return None

    # get {user_id}/{task_id}/{task_file_name}
    task_file_object_name = user_id + "/" + task_id + "/" + task_file_name
    task_file_blob = s3util.get_file_blob(bucket_name, task_file_object_name)
    if task_file_blob is None:
        print('get_task_file_blob: Failed to get file blob %s' % task_file_object_name)
        return None

    return task_file_blob


def upload_task_file(bucket_name, task, task_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('upload_task_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return ''

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return ''

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return ''

    # upload {user_id}/{task_id}/{task_file_name}
    task_file_object_name = user_id + "/" + task_id + "/" + task_file_name
    success = s3util.upload_file(task_file_name, bucket_name, task_file_object_name)
    if not success:
        print('upload_task_file: Failed to upload file %s.' % task_file_name)
        return ''

    # success
    return task_file_name


def download_task_file(bucket_name, task, task_file_attribute_name):
    bucket = s3util.get_bucket(bucket_name)
    if bucket is None:
        print('download_task_file: Bucket %s does not exist.' % bucket_name)
        return ''

    # get user_id, task_id, task_file_name
    user_id = get_task_attribute_value(task, 'user_id')
    if user_id == '':
        return ''

    task_id = get_task_attribute_value(task, 'task_id')
    if task_id == '':
        return ''

    task_file_name = get_task_attribute_value(task, task_file_attribute_name)
    if task_file_name == '':
        return ''

    # download {user_id}/{task_id}/{task_file_name}
    task_file_object_name = user_id + "/" + task_id + "/" + task_file_name
    success = s3util.download_file(bucket_name, task_file_object_name, task_file_name)
    if not success:
        print('download_task_file: Failed to download file %s.' % task_file_name)
        return ''

    # success
    return task_file_name

