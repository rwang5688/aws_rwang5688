import os
import s3util

def upload_asset_file(bucket_name, object_name):
    print('upload_asset_file: bucket_name=%s, object_name=%s' % (bucket_name, object_name))
    
    # extract local file name
    path = os.path.dirname(os.path.realpath(object_name))
    print('path: %s' % (path))
    upload_file_name = os.path.basename(os.path.realpath(object_name))
    print('upload_file_name: %s' % (upload_file_name))

    success = s3util.upload_file(upload_file_name, bucket_name, object_name)
    if not success:
        print('upload_cache_file: Failed to upload file %s.' % upload_file_name)
        return ''
    
    return upload_file_name


def upload_asset_files(asset_files):
    for asset_file in asset_files:
        bucket_name = asset_file['Bucket']
        object_name = asset_file['Key']

        upload_file_name = upload_asset_file(bucket_name, object_name)
        if upload_file_name == '':
            print('upload_asset_files failed: bucket_name=%s, object_name=%s.' % (bucket_name, object_name))
            return False
        
    return True

