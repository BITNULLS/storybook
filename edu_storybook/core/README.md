# `edu_storybook.core` Module Structure

This Python module is organized in the following manner:

 - `auth.py`: Contains all authentication and security related functions.
 - `bucket.py`: Functions to download, upload, and initialization for the storage bucket.
 - `config.py`: Just loads in the `config.json` file. Used to load in the main configuration file once.
 - `db.py`: Initialization of the database.
 - `helper.py`: Miscellaneous helper functions.
 - `reg_exps.py`: All regular expressions.
 - `remove_watchdog.py`: Script that launches a background process to handle deleting temporary files (usually user uploads, or generated files).
 - `sensitive.py`: All of our sensitive login information (security keys, accessing remote resources; Oracle Bucket, DB) is temporarily downloaded, loaded, and then deleted from here.

Additionally, there is the `data/` directory. 
As part of the main install, [you will need to download two sensitive data files](data/README.md).
