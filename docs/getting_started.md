# Getting Started

This file details how to setup, and understand the "flow" of this project.

Table of Contents:
 - [Setup](#setup)
 - [Developing](#developing)

## Setup

To get this server running, you need to follow these steps:

 1. [Download Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html).  This is the software driver to connect to the Oracle database.
 2. Unzip the Oracle Instant Client, and put it somewhere on your computer.
 3. Wherever you unzipped the Oracle Instant Client, `cd` into the directory, and `pwd` to get the working directory.  Copy the Oracle Instant Client full path (e.g. `/User/you/lib/instant_client/`)
 4. Create a file, `edu_storybook/core/data/oracle_dir.txt` in this repo.
 5. Paste the directory filepath of Oracle Instant Client in the `.txt`.
 6. [Download our `StorybookFiles.json`](https://drive.google.com/file/d/1HVrLbauaq_3jEqMXVs9yUFw0UIGSiPDP/view?usp=sharing) and place in `edu_storybook/core/data/`.
 7. [Download our `StorybookFiles.pem`](https://drive.google.com/file/d/14r0GyoITrOjcbVH_RaezkB8TL7gzBTfR/view?usp=sharing) and place in `edu_storybook/core/data/`.
 8. Run `make setup` in the root of the repository (`/`) directory to the install the necessary Python dependencies.  Or just run `pip3 install -r requirements.txt` for Windows.
    - If your `pip` command does not work (common problems with the `PATH` variable), then `python3 -m pip install -r requirements.txt` should be a foolproof command.
 9. [Install Poppler. **Follow the instructions on the page.**](https://pdf2image.readthedocs.io/en/latest/installation.html)
    - If you are on MacOS, and if you have `brew`, you can do `brew install poppler`
    - If you are on MacOS, and do not have `brew`, [install `brew`](https://brew.sh/), then `brew install poppler`.
 9. You're all done!  Now execute `make run` to start the server.
    - **NOTE**: If it does not work, try `flask run`
    - **NOTE**: If it still does not work, you can just run `app.py` directly. You will have to `cd edu_storybook` and then `python3 app.py`.
 10. Flask may have trouble running, so you will have to execute all of the `make run` commands one by one, copying from the makefile.

## Developing

To develop in this app, there are few things to understand that are unique to this project.

 1. All of the webpages are server-side generated, meaning the user is effectively stateless. The user is served each webpage, the data is purely held in the database, and a small amount of data in the user's login session cookie. Everything else is interpreted and computed by the Flask server.
    - [**Please** read this article from Mozilla on server-side websites.](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Introduction) It's short, yet thorough, and should answer any questions you have.
 2. All of the webpages that are generated are only in the `edu_storybook/*.py` files, top-level `edu_storybook` module.
 3. The `edu_storybook.core` module holds functions used throughout the app.
 4. The `edu_storybook.api` module holds many endpoints responsible for a mix of server-side generated and AJAX behaviors, mostly AJAX.
 5. If you save (Win: `Ctrl + S`, MacOS: `Cmd + S`) any `edu_storybook` Python script file, it will reload the web server.
 6. If you save any template file in `edu_storybook/templates/`, it will **NOT** reload the web server.

 ## Setting up SQL Developer DB Connection

 1. Open **SQLDeveloper application**.
 2. On the top left corner of the *Home Page* of **SQLDeveloper** and under *Connections* tab, click on the **green plus sign (+)** to create a new connection.
 3. A dialog box saying *New/Select Database Connection* will open up. There are some fields that we need to fill out to ensure that our new connection works smoothly.
 4. On the *Name* field, give any convenient name to your Database connection which would be helpful for you later to remember.
 5. Next, let the *Database Type* be *Oracle*. 
 6. Next, given two tabs (*User Info* and *Proxy User*), click on the *User Info* tab.
 7. Now we would fill out some fields under the *User Info* Tab. First, let the *Authentication Type* and *Role* be set to *Default*.
 8. Second, fill out the *Username* field as *kpelster* (all lowercase).
 9. And third, fill out the *Password* field as *KaraPelster1234* (both password and username should be written as provided) .
 10. Optionally, if you want, you can also put checkmark on *Save Password* field if you want password to be remembered whenever you disconnect and then re-connect your DB connection. 
 11. We are basically done with *User Info* tab and will now fill out the last section, *Connection Type*, to create our new DB connection successfully.
 12. First off, change the *Connection Type* from *Basic* to *Cloud Wallet*. 
 13. Next, given three tabs (*Details*, *Advanced*, and *Proxy*), click on the *Details* tab if you are not already on that tab.
 14. Now, for the *Configuration File* field, we need to make sure that we point to where our *Wallet_EDUStorybook.zip* file is on our system. We need to make sure that *Wallet_EDUStorybook.zip* file is placed securely on our system. Deletion of this file could result in our DB connection not working properly or maybe completely. 
 15. Once we point to the location of *Wallet_EDUStorybook.zip* file for *Configuration File* field, the *Service* field (below *Configuration File* field) automatically fills to *edustorybook_high* value. DON'T CHANGE THAT VALUE AND KEEP IT AS IT IS.
 16. Similarly, we don't need to do anything with *Configure OSS Classic* and can just ignore it.
 17. Now we are good to go for testing our DB Connection by clicking **Test** button from the below few buttons.
 18. At this point, the *Status* field should be *Success* and we can now click on **Connect** button to successfully create our new DB connection.