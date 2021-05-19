import os
import json
import copy
import uuid
from pathlib import Path


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

    revision = copy.deepcopy(revision_manifest)
    print('Revision:')
    print(revision)

    manifest = revision['Manifest']
    print('Manifest:')
    print(manifest)


if __name__ == '__main__':
    main()

