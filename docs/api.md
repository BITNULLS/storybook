# EduStorybook API Documentation

Below is the specification of all API endpoints, their expected inputs, 
conditions and returns.

Table of Contents:
 - [Meta Notes](#meta_notes)
 - [`/book`](#book)
 - [`/login`](#login)
 - [`/password/forgot`](#password-forgot)
 - [`/password/reset`](#password-reset)
 - [`/admin/download/user`](#admin-download-user)
 - [`/admin/download/action`](#admin-download-action)
 - [`/admin/book/upload`](#admin-book-upload)
 - [`/admin/book/download`](#admin-book-download)
 - [`/admin/page`](#admin-page)
 - [`/admin/book/grant`](#admin-book-grant)
 - [`/quiz/submit`](#quiz-submit)

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

## Book
`POST \book`

This retrieves all books that the user has access to.

### Inputs
None

### Returns
On success,
```
{
    "status": "ok"
}
```

It has a data object which contains all the book_id's to the books the user has access to.

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


## Register

`POST /register`

This allows a new user to create an account.

### Inputs

- `email`: user's email
- `password`: password to be used
- `first_name`: user's first name
- `last_name`: user's last name
- `school_id`: user's study they are participating in

### Returns

On success, returns

```
 return {
        "status": "ok"
    }
```

emails the new user with a confirmation email. If not, returns "status": "fail" for the following conditions:

1. Email, password, first name, last name, or school study was not provided.
2. Email failed sanitization check of more than 8 characters &/or alphanumeric.
3. Error when querying database.
4. Email is already registered to an account.
5. Error when querying into database.

## Password Forgot

`POST /password/forgot/`

This lets a user reset a password.

### Inputs 

- `email`: user email

### Returns

On success, returns 

```
 return {
        "status": "ok"
    }
```

if an email is a match, then sends a link to the password/reset endpoint. If not, returns "status": "fail" for the following conditions:

1. Email was not provided.
2. Email failed sanitization check of more than 8 characters &/or alphanumeric.
3. Error when querying database.
4. No email matches what was passed.
5. Error when querying database.


## Password Reset

`POST /password/reset/`

This lets a user change their password.

### Inputs 

- `new_pass`: new password
- `confirm_pass`: confirm password
- `reset_key`: 512 random byte string

### Returns

On success, returns 

```
 return {
        "status": "ok"
    }
```

resets the password in database. If not, returns "status": "fail" for the following conditions:

1. Either password was not provided.
2. Either one or both passwords failed sanitization check of more than 8
    characters &/or alphanumeric.
3. Both passwords do not match.
4. Error when querying database.
5. No reset_key matches what was passed.
6. Error when querying database.
7. Error when querying database.

## Get Storyboard Page Count
`Get /storyboard/pagecount/<int:book_id_in>`

### Inputs

- `book_id_in`: a book number

### Returns 

On success, returns 
```
    "pagecount": int
```

But this can fail because of,
 2. `book_id` is not clean
 3.  Error when connecting to database

## Get Storyboard Page
`Get /storyboard/page/<int:book_id_in>/<int:page_number_in>`

### Inputs

- `book_id`: a book number
- `page_number`: a next or prev page (have to do math in front end)

### Returns 

On success, returns a png


But this can fail because of,
 2. `book_id` or `page_number` is not clean
 3.  Error when connecting to database
 4.  No image found in that location in the bucket

## storyboard/action/

`POST /storyboard/action`

This saves a user action. 

### Inputs 

- `detail_description`: Description of action.
- `book_id`: A book number.
- `action_id`: A user action.
- `action_start`: A epoch time of when action started. (In format YYYY-MM-DD HH:MM:SS)
- `action_stop`: A epoch time of when action stopped. (In format YYYY-MM-DD HH:MM:SS)

### Returns

On success, returns

```
{
    "status": "ok"
}
```

But this can fail because of,
 1. `book_id`, `detail_description`, `action_key_id`, `action_start`, and `action_stop` is not provided
 2. `book_id` or `action_key_id` is not clean
 3. `action_start`,`action_stop`, or `detail_description` is not clean
 4.  Error when uploading file

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

## quiz/submit

`POST /quiz/submit`

Inserts a user's quiz answer into the user_response table.

### Inputs 

 - `answer_id` - ID of the answer to the given question
 - `question_id` - ID of the question being answered

### Returns

On success,

```
{
    "status": "ok"
}
```

But this can fail because of,

 4. Either the `answer_id` or `question_id` is not provided
 5. `answer_id` or `question_id` is not clean (invalid characters)
 6. No `answer_id` or `question_id` matches found

## admin/book/upload/

`POST /admin/book/upload/`

Allows admin user to upload file to bucket

### Inputs

This form data must specifically be in the type of `multipart/form-data`.

 - `book_name`: The name of the book to be stored in the database.
 - `book_description`: The description of the book to be displayed in the dashboard.
 - `study_id`: The study the book will belong to.
 - `file`: The book file itself, e.g. `<input type=file name=file>`.

### Returns

On Success, 

```
{
    "status": "ok",
    "message": "file uploaded"
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
    "status": "ok",
    "message": "file downloaded"
}
```

When testing with postman, the input filename is set in the request Body form-data. The key should be called "file" and should be of type Text. Then, enter the exact filename of the file to be downloaded as the value.

Failure may occur because of,

14. File could not be downloaded

## admin-page

`POST /admin/page`

Allows admin user to upload a question and answers.

### Inputs

- `question_in` : full text question
- `school_id_in` : school id that questions belong to
- `book_id_in` : book id that questions belong to
- `page_prev_in` : previous page before question
- `page_next_in` : next page after question
- `answers_in` : all answers, separated by {space}{tilde}{back tick}{tilde}{space} (that is `` ~`~ ``).

### Returns 

On Success, 
```
{
    "status": "ok:
}
```

When testing on postman, the inputs should be set in the request body form-data exactly keys as defined as above. They should be of type text. 'answers_in' must be a string of delimited answers. For example, if the three answers are red, green and purple, 'answers_in' should be input as ``red ~`~ green ~`~ purple ~`~ ``.

Failure may occur because of,

2. school_id, book_id_in, page_prev_in, or page_next_in are not integers

`PUT /admin/page`

Allows user to edit questions and answers

### Inputs

- `question_id_in` : question id that is being edited
- `question_in` : full text question
- `answers_in` : all answers and their ids. The format of this string is as follows {answer_id}++{answer}{space}{tilde}{back tick}{tilde}{space}{answer_id}++{answer}.... and so on (that is ``10++answer1 text ~`~ 11++answer2 text ~`~ 11++answer3 text``). This allows there to be an arbitrary number of answers to be edited. This delimiters here are obnoxious, but they are important for distinguishing delimiter versus real user text.

When testing on postman, the inputs should be set in the request body form-data exactly keys as defined as above. They should be of type text. 'answers_in' must be a string of properly delimited answers. For example, if the three answers are red, green and purple with ids 1, 2, and 3, 'answers_in' should be input as ``1++red ~`~ 2++green ~`~ 3++purple ~`~ ``.

Failure may occur because of,

1. not all inputs are provided
2. question_id is not an integer

### Returns 

On Success, 
```
{
    "status": "ok:
}
```

`DELETE /admin/page`

Allows admin user to delete questions and answers given a question id

### Inputs 

 - `question_id_in`: number id for a question

### Returns 

```
{
    "status": "ok"
}
```

When testing with postman, the input question id is set in teh request Body form-data. The key should be "question_id_in" and be of type text.

Failure may occur because of,

2. question_id_in is not of type int.
5. Request type is not GET, PUT, POST, or DELETE.

## /admin/book/grant

`POST /admin/book/grant`

Allows admin user to upload a book that is associated with a study id.

### Inputs

 - `book_name`: Text of full name of book.
 - `book_url`: Text of full url for book.
 - `book_description`: Text of full description for book.
 - `study_id`: Number id for the study that the book belongs to

### Returns

On Success, 

```
{
    "status": "ok"
}
```

When testing with postman, the inputs will be input in "form-data" as text inputs. Enter the same exact input variables as above into the key column. Then, supply inputs to the value column.

4. Failure may occur if the input study_id does not exist in the table STUDY since the parent key will not be found.

## /admin/get/user/

`GET /admin/get/user/`

Allows admin user to get a list of the next 50 users based on date the user was created.

### Inputs

 - `offset`: Int to offset by (multiple of 50).

### Returns

On Success, 

```
{
    "status": "ok"
    "users" : [
        {
            "EMAIL" : ...
            "STUDY_ID": ...
            "USER_ID": ...
        }, ...
    ]
}
```
User objects have 3 attributes:
 - `EMAIL`: string with @ for login attached to user 
 - `STUDY_ID`: Int of study
 - `USER_ID` : string given whe user created
Returns a list of next 50 users in JSON format. 

1. Failure if an offset was not provided
2. Failure if offset is not an integer
3. Failure when connecting to database

## /admin/get/schools/

`GET /admin/get/schools`

Allows user to get a list of the next 50 schools based on alphebetical order of the school names.

### Inputs

 - `offset`: Int to offset by (multiple of 50).

### Returns

On Success, 

```
{
    "schools" : [
        "schoolA",
        "schoolB",
        ...
    ]
}
```
Where:
 - `SchoolName`: string that is name of school in database 
 
Returns a list of next 50 schools in JSON format. 

1. Failure if an offset was not provided
2. Failure if offset is not an integer
3. Failure when connecting to database
