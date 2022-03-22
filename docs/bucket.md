# Storybook Backend Server

This directory contains all the code to run the backend server, as well as unit
tests to ensure it's reliability and security.

[If you're looking for the API endpoints, click here.](api.md)

## How to Upload/Download/Delete/List from the Bucket

### Bucket Configurations Files

Requirements/Steps to use the Chum-Bucket:
 - Download our oracle_bucket.json and Chum-Bucket.pem, and place the files in backend/data/. These files contain the information to connect to our Cloud Bucket. This will allow you to use the functions `upload_bucket_file` and `download_bucket_file` in `edu_storybook/bucket.py`.

### Upload File to Cloud

To upload, the function `upload_bucket_file` is used. It is located in `edu_storybook/bucket.py`.

To upload files, you will need "poppler". Review https://pdf2image.readthedocs.io/en/latest/installation.html to see how you can download poppler on your machine. MacOS can simply use "brew install poppler". Windows will have to download the package first (but this is in the link).

 - The function takes 2 parameter:
   - `local_file_path`: string of the local path of file to upload 
   - `cloud_file_name`: string of the new name of file in Chum-Bucket
 - The function will return a boolean, depending on if the file was uploaded or not.

### Download File to Local Machine

To download, the function `download_bucket_file` is used. It is located in `edu_storybook/bucket.py`.

 - The function takes a single parameter:
   - `filename`: string of the name of the file in Chum-Bucket
 - This will download the given file into the folder `bucket_files/`
   - If the folder is not present, it will be created automatically.
   - If the object does not exist in the bucket, `None` will be returned.

### Delete File in Cloud

To delete a file in the bucket, the function `delete_bucket_file` is used. It is located in `edu_storybook/bucket.py`.

 - The function takes a single parameter:
   - `filename`: string of the file to delete from Chum-Bucket
 - The function returns a boolean
   - True if the file is deleted
   - False if the file is not deleted or does not exist in the
 - This will **permanently remove** the file from the bucket.
   - **BE CAREFUL**

### List Bucket Contents

 To check the contents of the bucket, the function `list_bucket_files` is used. It is located in `edu_storybook/bucket.py`.

 - The function takes no parameters and returns a list containing the names of the objects in the bucket.
 - If the bucket is empty, it will return `None`

## Notes

 - **Critical**: In `edu_storybook/core/data/` there needs to be a `oracle_key.json` file
 - **Critical**: In `edu_storybook/core/data/` there needs to be a `oracle_dir.txt` file
 - We are using Python `3.x`
 - Yes, getting the Oracle Database client working is an absolute pain in the caboose, and this is the way it is meant to be done
 - Our current test login is `test@udel.edu` and password `password`.
 - The sensitive files are downloaded from the cloud
   - The only file that are needed to download the other files are `StorybookFiles.json` and `StorybookFiles.pem`