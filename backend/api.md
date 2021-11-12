# EduStorybook API Documentation

Below is the specification of all API endpoints, their expected inputs, 
conditions and returns.

Table of Contents:
 - [Meta Notes](#meta_notes)
 - [`login/`](#login)
 - [`admin/download/user/`](#admin/download/user)
 - [`admin/download/action/`](#admin/download/action)
 - [`admin/book/upload/`](#admin/book/upload)
 - [`admin/book/download/`](#admin/book/download)

## Meta Notes

 - This API does not serve the frontend web app.
 - It just handles requests from the live frontend to the database.
 - Requests are sent to the backend in `application/x-www-form-urlencoded`.
 - Responses are sent back to the front in `application/json`.

**When a request fails**, the server will return back a `json` response in this standard form:

```
{
    "status": "fail",
    "fail_no": 1,
    "message": "...",
    ["database_message": "..."]
}
```

**When a request succeeds**, the server will return back `json` response in this standard form:

```
{
    "status": "ok",
    ...
}
```

## Authorization

When users are authenticated by the `POST /login` endpoint, they are given a JSON Web Token (JWT) that holds the following information:

```
{
    "iat": Issue At Time, when this token was issued
    "session": SESSION_ID in the USER_SESSION table
    "sub": USER_ID of the user
    "permission": ADMIN of the user
}
```

## Login

`POST /login`

This lets a user login.

### Inputs

 - `email`: A user email.
 - `password`: A user password.

### Returns

On success,

```
{
    "status": "ok",
    "message": "Successfully authenticated",
    "sub": user_id
}
```

Two things happen:
 - An **`Authorization: Bearer <token>`** cookie is set, which validates your login session.

But this can fail because of,

 1. Either the email or password is not provided
 2. Email or password is not clean (invalid characters)
 3. Error when querying the database
 4. No email matches found
 5. Password incorrect
 6. Error when updating the database

## admin/download/user/

`POST /admin/download/user`

This lets an admin download user data as a csv.

### Inputs 

none

### Returns

On success, returns a CSV file.

The user must be properly authenticated as an admin user. To be authenticated, they must first login in with their email and password to establish a cookie. See [`login/`](#login) above. 

## admin/download/action/

`POST /admin/download/action`

This lets an admin download user data as a csv. 

### Inputs 

none

### Returns

On success, returns a CSV file.

The user must be properly authenticated as an admin user. To be authenticated, they must first login in with their email and password to establish a cookie. See [`login/`](#login) above. 

## admin/book/upload/

`POST /admin/book/upload/`

Allows admin user to upload file to bucket

### Inputs

 - `file`: A file.

### Returns

On Success, 

```
{
    "message": "file uploaded",
    "status": "success"
}
```

When testing in Postman, the input file should be input into the body form-data. The key should be "file" with type "File". If you successfully change the type of the key to a file type, the value column will allow you to select a file from your machine.

To ensure that a valid file is selected the code checks that a request file exists, that the filename is not an empty string, and that the file extension is pdf, ppt, or pptx.

Failure may occur because of,

10. No file was found in request.files
11. The filename is an empty string
12. Error when uploading file
13. File is not of valid format or file is invalid


## admin/book/download/

`POST /admin/book/download/`

Allows admin user to download a book from the file bucket.

### Inputs

 - `file`: A file.

### Returns

On Success, 

```
{
    "status": "success",
    "message": "file downloaded"
}
```

When testing with postman, the input filename is set in the request Body form-data. The key should be called "file" and should be of type Text. Then, enter the exact filename of the file to be downloaded as the value.

Failure may occur because of,
14. File could not be downloaded