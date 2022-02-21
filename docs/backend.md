# Storybook Backend Server

This directory contains all the code to run the backend server, as well as unit
tests to ensure it's reliability and security.

[If you're looking for the API endpoints, click here.](api.md)

## Setup

To get this server running, you need to follow these steps:

 1. [Download Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html).  This is the software driver to connect to the Oracle database.
 2. Unzip the Oracle Instant Client, and put it somewhere on your computer.
 3. Wherever you unzipped the Oracle Instant Client, `cd` into the directory, and `pwd` to get the working directory.  Copy the Oracle Instant Client full path (e.g. `/User/you/lib/instant_client/`)
 4. Create a file, `backend/data/oracle_dir.txt` in this repo.
 5. Paste the directory filepath of Oracle Instant Client in the `.txt`.
 6. [Download our `StorybookFiles.json`](https://drive.google.com/file/d/1HVrLbauaq_3jEqMXVs9yUFw0UIGSiPDP/view?usp=sharing) and place in `backend/data/`.
 7. [Download our `StorybookFiles.pem`](https://drive.google.com/file/d/14r0GyoITrOjcbVH_RaezkB8TL7gzBTfR/view?usp=sharing) and place in `backend/data/`.
 8. Create a `domain.txt` in the `backend/data/` folder, such that `backend/data/domain.txt` file exists.
 9. Run `make setup` in this `backend/` directory to the install the necessary Python dependencies.  Or just run `pip3 install -r requirements.txt` for Windows.
 10. [Install `cloudflared` according to these instructions.](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation)
 11. You're all done!  Now execute `make run` to start the server.
 12. Flask may have trouble running, so you will have to execute all of the `make run` commands one by one, copying from the makefile.

## How to Test the API

For now, we will use Postman to send test requests to the backend server.

 1. [Download the Postman client](https://www.postman.com/downloads/)
 2. For the first time only: Run Postman, and select `Skip login...`
 3. In the top middle of the Postman client, click the circular satellite icon.
 4. Click the `Use interceptor` button.
 5. Install the `Postman Interceptor` client into your web browser.
 6. Go back to Postman, and click on the circular satellite icon, then click the `Use interceptor` button.
 7. The satellite icon should turn orange.
 8.  In a terminal, run the command `cloudflared tunnel --url http://localhost:5000`
 9.  Copy the url that Cloudflare gives you in the box, it looks like `https://word1-word2...trycloudflare.com/`
 10. Paste in the `Enter request URL` field of Postman.
 11. Paste it in the `backend/data/domain.txt` file you created.
 12. Make sure the backend server is actually running with `make run`
 13. **Critical**: To test POST form data, use `Body` tab, and select the `x-www-form-urlencoded` option.
 14. **Critical**: In the `Headers` tab, add a new key value pair: Key=`Origin` and value=`localhost`.

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

 - **Critical**: In `backend/data/` there needs to be a `oracle_key.json` file
 - **Critical**: In `backend/data/` there needs to be a `oracle_dir.txt` file
 - We are using Python `3.x`
 - Yes, getting the Oracle Database client working is an absolute pain in the caboose, and this is the way it is meant to be done
 - Our current test login is `test@udel.edu` and password `password`.
 - The sensitive files are downloaded from the cloud
   - The only file that are needed to download the other files are `StorybookFiles.json` and `StorybookFiles.pem`