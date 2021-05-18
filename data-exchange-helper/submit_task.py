import os
import json
import copy
import uuid
from pathlib import Path
import cachefile
import taskfile
import taskmessage


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s' % env_var_name)
    return env_var


def get_env_vars():
    global preprocess_bucket_name
    global cache_bucket_name
    global result_bucket_name
    global create_task_queue_name
    global xcalibyte_dir_name

    preprocess_bucket_name = get_env_var('TASK_EXEC_PREPROCESS_DATA_BUCKET')
    if preprocess_bucket_name == '':
        return False

    cache_bucket_name = get_env_var('TASK_EXEC_CACHE_DATA_BUCKET')
    if cache_bucket_name == '':
        return False

    result_bucket_name = get_env_var('TASK_EXEC_RESULT_DATA_BUCKET')
    if result_bucket_name == '':
        return False

    create_task_queue_name = get_env_var('TASK_EXEC_CREATE_TASK_QUEUE')
    if create_task_queue_name == '':
        return False

    xcalibyte_dir_name = get_env_var('XCALIBYTE_DIR_NAME')
    if xcalibyte_dir_name == '':
        return False

    # success
    return True


def parse_arguments():
    import argparse
    global task_conf_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('task_conf_file_name', help='task conf file name.')

    args = parser.parse_args()
    task_conf_file_name = args.task_conf_file_name

    if task_conf_file_name is None:
        print('parse_arguments: task_conf_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def upload_preprocess_files(task):
    task_file_attribute_name = 'task_fileinfo_json'
    task_file_name = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_preprocess_files failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_preprocess_tar'
    task_file_name = taskfile.upload_task_file(preprocess_bucket_name, task, task_file_attribute_name)
    if task_file_name == '':
        print('upload_preprocess_files failed: %s.' % task_file_attribute_name)
        return False

    task_file_attribute_name = 'task_source_code_zip'
    if task_file_attribute_name in task:
        task_file_name = taskfile.upload_task_file(result_bucket_name, task, task_file_attribute_name)
        if task_file_name == '':
            print('upload_preprocess_files failed: %s.' % task_file_attribute_name)
            return False
    else:
        print('upload_preprocess_files: No need to upload source code package')

    # success
    return True


def upload_cache_files(task):
    # cache: java_rt_lib
    cache_name = 'java_rt_lib'
    cache_id_attribute_name = 'java_rt_lib_id'
    cache_file_attribute_name = 'java_rt_lib_tar'
    if cache_file_attribute_name not in task:
        print('upload_cache_files: No need for cache %s.' % cache_name)
        return True

    if cachefile.file_exists(cache_bucket_name, task,
                        cache_name, cache_id_attribute_name, cache_file_attribute_name):
        print('upload_cache_files: File exists for %s.' % cache_file_attribute_name)
        return True

    cache_id = cachefile.get_task_attribute_value(task, cache_id_attribute_name)
    if cache_id == '':
        return True

    cache_file_name = cachefile.get_task_attribute_value(task, cache_file_attribute_name)
    if cache_file_name == '':
        return True

    xcalibyte_path = os.path.join(str(Path.home()), xcalibyte_dir_name, cache_id)
    if not os.path.exists(xcalibyte_path):
        print('upload_cache_files: Path does not exist for %s.' % xcalibyte_path)
        if os.path.exists(cache_file_name):
            xcalibyte_path = None
            print("upload_cache_files: Use file in path %s" % os.path.join(os.getcwd(), cache_file_name))
        else:
            return True

    upload_file_name = cachefile.upload_cache_file(cache_bucket_name, task,
                        cache_name, cache_id_attribute_name, cache_file_attribute_name,
                        local_cache_dir=xcalibyte_path)
    if upload_file_name == '':
        # error
        print('upload_cache_files: File upload failed for %s.' % cache_file_attribute_name)
        return False

    # success
    return True


def main():
    print('\nStarting submit_task.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('preprocess_bucket_name: %s' % preprocess_bucket_name)
    print('cache_bucket_name: %s' % cache_bucket_name)
    print('result_bucket_name: %s' % result_bucket_name)
    print('create_task_queue_name: %s' % create_task_queue_name)
    print('xcalibyte_dir_name: %s' % xcalibyte_dir_name)

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print('task_conf_file_name: %s' % task_conf_file_name)

    task_conf = get_json_data(task_conf_file_name)
    if task_conf is None:
        print('get_json_data failed.  Exit.')
        return

    task = copy.deepcopy(task_conf)
    task_id = task['task_id']
    if task_id == 'uuid':
        # need to generate task_id
        task_id = str(uuid.uuid4())
        task['task_id'] = task_id

    print('Task:')
    print(task)

    success = upload_preprocess_files(task)
    if not success:
        print('upload_preprocess_files failed: task=%s.  Exit.' % task)
        return

    success = upload_cache_files(task)
    if not success:
        print('upload_cache_files failed: task=%s.  Exit.' % task)
        return

    action = 'create'
    success = taskmessage.send_task_message(create_task_queue_name, action, task)
    if not success:
        print('send_task_message failed.  Exit.')
        return


if __name__ == '__main__':
    main()

