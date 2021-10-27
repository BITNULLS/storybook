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
 6. [Download our `oracle_key.json`](https://drive.google.com/file/d/1o50RcKhDWeBZyKIsH-BwOy_yQVb79pcb/view?usp=sharing), and place the file in `backend/data/`.  So you should have `backend/data/oracle_key.json`.  Keep this safe.  This contains the username, password, and URL to connect to the database.  
 7. [Download our `Wallet_EDUStorybook` wallet](https://drive.google.com/file/d/15tEPQTOutgKm5h2kJP3hRE4VO8czimP4/view?usp=sharing), and place the zip in `backend/data/` and unzip it. So you should have `backend/data/Wallet_EDUStorybook/`.  Keep this safe.  This contains the certificates necessary to authenticate a database connection.
 8. Run `make setup` in this `backend/` directory to the install the necessary Python dependencies.  Or just run `pip3 install -r requirements.txt` for Windows.
 9. [Install `cloudflared` according to these instructions.](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation)
 10. You're all done!  Now execute `make run` to start the server.
 11. Flask may have trouble running, so you will have to execute all of the `make run` commands one by one, copying from the makefile.

## How to Test the API

For now, we will use Postman to send test requests to the backend server.

 1. [Download the Postman client](https://www.postman.com/downloads/)
 2. For the first time only: Run Postman, and select `Skip login...`
 3. In the top middle of the Postman client, click the circular satellite icon.
 4. Click the `Use interceptor` button.
 5. Install the `Postman Interceptor` client into your web browser.
 6. Go back to Postman, and click on the circular satellite icon, then click the `Use interceptor` button.
 7. The satellite icon should turn orange.
 8. Make sure the backend server is actually running with `make run`
 9.  In a terminal, run the command `cloudflared tunnel --url http://localhost:5000`
 10. Copy the url that Cloudflare gives you in the box, it looks like `https://word1-word2...trycloudflare.com/`
 11. Paste in the `Enter request URL` field of Postman.
 12. **Critical**: To test POST form data, use `Body` tab, and select the `x-www-form-urlencoded` option.
 13. **Critical**: In the `Headers` tab, add a new key value pair: Key=`Origin` and value=`localhost`.

## Notes

 - **Critical**: In `backend/data/` there needs to be a `oracle_key.json` file
 - **Critical**: In `backend/data/` there needs to be a `oracle_dir.txt` file
 - We are using Python `3.x`
 - Yes, getting the Oracle Database client working is an absolute pain in the caboose, and this is the way it is meant to be done
 - Our current test login is `test@udel.edu` and password `password`.