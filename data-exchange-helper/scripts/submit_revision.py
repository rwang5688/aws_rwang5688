import os
import json
import copy
import uuid
from pathlib import Path
import assetfile
import s3util


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s' % env_var_name)
    return env_var


def get_env_vars():
    global manifest_bucket_name

    manifest_bucket_name = get_env_var('MANIFEST_BUCKET')
    if manifest_bucket_name == '':
        return False

    # success
    return True


def parse_arguments():
    import argparse
    global revision_manifest_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('revision_manifest_file_name', help='revision manifest file name.')

    args = parser.parse_args()
    revision_manifest_file_name = args.revision_manifest_file_name

    if revision_manifest_file_name is None:
        print('parse_arguments: revision_manifest_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def main():
    print('\nStarting submit_revision.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('manifest_bucket_name: %s' % manifest_bucket_name)

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print('revision_manifest_file_name: %s' % revision_manifest_file_name)

    revision_manifest = get_json_data(revision_manifest_file_name)
    if revision_manifest is None:
        print('get_json_data failed.  Exit.')
        return

    print('%s:' % revision_manifest_file_name)
    print(revision_manifest)

    manifest = revision_manifest['Manifest']
    if manifest is None:
        print('Manifest does not exist.  Exit.')
        return

    asset_files = manifest['Assets']
    if asset_files is None:
        print('Assets do not exist.  Exit.')
        return    

    print('Assets:')
    print(asset_files)

    success = assetfile.upload_asset_files(asset_files)
    if not success:
        print('upload_asset_files failed.  Exit.')
        return

    success = s3util.upload_file(revision_manifest_file_name, manifest_bucket_name, revision_manifest_file_name)
    if not success:
        print('upload_file: Failed to upload file %s.' % revision_manifest_file_name)
        return ''


if __name__ == '__main__':
    main()

