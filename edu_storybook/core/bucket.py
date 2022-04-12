"""
bucket.py

Launches connection to Oracle Bucket, where we store large data files.
Provides simple functions for accessing the bucket.
"""

import oci
import json
import os
from .filepath import fix_filepath
from tempfile import TemporaryDirectory
from typing import List
from .config import config, temp_folder

import logging

c_bucket_log = logging.getLogger('core.bucket')
if config['production'] == False:
    c_bucket_log.setLevel(logging.DEBUG)

# Sen_Files Downloader setup - Only used to download project configuration files
# Chum-Bucket Downloader will be set up after config files have been downloaded

with open(fix_filepath(__file__, 'data/StorybookFiles.json')) as sb_files:
    bucket = json.load(sb_files)

assert bucket is not None, 'StorybookFiles.json file was empty'

sen_config = bucket['config']
sen_config['key_file'] = fix_filepath(__file__, sen_config['key_file'])

oracle_cloud_client = oci.object_storage.ObjectStorageClient(sen_config)

def upload_bucket_file(local_file_path: str, cloud_file_name: str) -> int:
    """
    Uploads local file to cloud bucket
    :param local_file_path: path to local file to upload
    :param cloud_file_name: Name for file in cloud
    :return: the http status code of the upload response
    """
    with open(local_file_path, 'rb') as fh:
        return oracle_cloud_client.put_object(bucket['namespace'], bucket['name'], cloud_file_name, fh).status


def download_bucket_file(filename: str, folder = temp_folder) -> str:
    """
    Downloads files from cloud bucket
    :param filename: The name of the file to download
    :return: the local path of the downloaded file, None if there is an error
    """
    if not os.path.isdir(folder):
        os.mkdir(folder)

    try:
        obj = oracle_cloud_client.get_object(bucket['namespace'], bucket['name'], filename)
        if filename[filename.rfind('/')+1:] != -1:
            filename = filename[filename.rfind('/')+1:]
        new_file = folder + '/' + filename
        with open(new_file, 'wb') as f:
            for chunk in obj.data.raw.stream(1024*1024, decode_content=False):
                f.write(chunk)
            f.close()
        return new_file
    except oci.exceptions.ServiceError as e:
        c_bucket_log.warning("The object '" + filename + "' does not exist in bucket.")
        return None


def delete_bucket_file(filename: str) -> bool:
    """
    Deletes a given file in Chum-Bucket
    :param filename: Filename of file to delete in Chum-Bucket
    :return: Boolean depending on if the file was deleted or not.
    """
    try:
        oracle_cloud_client.delete_object(bucket['namespace'], bucket['name'], filename)
        return True
    except oci.exceptions.ServiceError as e:
        c_bucket_log.warning("The object '" + filename + "' does not exist in bucket.")
        return False


def list_bucket_files() -> List[str]:
    """
    Prints each object in the bucket on a separate line. Used for testing/checking.
    :return: List of filenames, if bucket is empty returns None
    """
    files = oracle_cloud_client.list_objects(bucket['namespace'], bucket['name'])
    file_names = []
    get_name = lambda f: f.name
    for file in files.data.objects:
        file_names.append(get_name(file))
    return file_names

temp_dir = TemporaryDirectory()
temp_dir_name = temp_dir.name

wallet = download_bucket_file("Wallet_EDUStorybook.zip", temp_dir_name)
domain = download_bucket_file("domain.txt", temp_dir_name)
email = download_bucket_file("email.password", temp_dir_name)
jwt = download_bucket_file("jwt.key", temp_dir_name)
oracle_key = download_bucket_file("oracle_key.json", temp_dir_name)

# Download Bucket Configuration Files
chum_pem = download_bucket_file("Chum-Bucket.pem", temp_dir_name)
oracle_bucket = download_bucket_file("tfolder_oracle_bucket.json", temp_dir_name)

# Chum-Bucket Uploader/Downloader setup
with open(oracle_bucket) as bucket_details:
    bucket = json.load(bucket_details)
assert bucket is not None, 'oracle_bucket.json file was empty'
bucket_config = bucket['config']
bucket_config['key_file'] = temp_dir_name + '/' +bucket_config['key_file']
oracle_cloud_client = oci.object_storage.ObjectStorageClient(bucket_config)
os.remove(chum_pem)
os.remove(oracle_bucket)
