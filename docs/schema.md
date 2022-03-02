# Database Schema Documentation

Below is documentation for the oracle database schema.

Table of Contents:
 - [`ACTION`](#ACTION)
 - [`ACTION_DETAIL`](#ACTION_DETAIL)
 - [`ACTION_KEY`](#ACTION_KEY)
 - [`ANSWER`](#ANSWER)
 - [`BOOK`](#BOOK)
 - [`PASSWORD_RESET`](#PASSWORD_RESET)
 - [`QUESTION`](#QUESTION)
 - [`SCHOOL`](#SCHOOL)
 - [`STUDY`](#STUDY)
 - [`USER_PROFILE`](#USER_PROFILE)
 - [`USER_RESPONSE`](#USER_RESPONSE)
 - [`USER_SESSION`](#USER_SESSION)

<br>

# ACTION

|  column name | description  | 
|---|---|
| USER_ID | ID to identify a user from [`USER_PROFILE`](#USER_PROFILE) |
| ACTION_START | The time that user began the action  |
| ACTION_STOP | The time that the user stopped the action  |
| BOOK_ID | ID of a book from [`BOOK`](#BOOK) that the user enacted the action upon |
| DETAIL_ID | ID of an action detail from [`ACTION_DETAIL`](#ACTION_DETAIL) | \

<br>

# ACTION_DETAIL

|  column name | description  | 
|---|---|
| DETAIL_ID | Number ID to uniquely identify the detail |
| DETAIL_DESCRIPTION | Text description of the specifics about a user action |
| ACTION_KEY_ID | ID of an action from  [`ACTION_KEY`](#ACTION_KEY)|

<br>

# ACTION_KEY

|  column name | description  | 
|---|---|
| ACTION_KEY_ID | Number ID to uniquely identify the action|
| ACTION_NAME | Short hand name of action |

<br>

# ANSWER

|  column name | description  | 
|---|---|
| ANSWER_ID | Unique number ID to uniquely identify the answer|
| QUESTION_ID | ID to a question in [`QUESTION`](#QUESTION) that the answer is related to|
| ANSWER | Full text of answer |
| CORRECT | Identifies if an answer to a particular QUESTION_ID is correct. 1 if correct. 0 if they are not correct |

<br>

# BOOK

|  column name | description  | 
|---|---|
| BOOK_ID | Unique number ID to uniquely identify the book |
| BOOK_NAME | Full name of book |
| CREATED_ON | Date that the book was added to site |
| URL | Filepath to the book in the file bucket |
| DESCRIPTION | Text description of the book |
| STUDY_ID | ID of the study from [`STUDY`](#STUDY) that the book belongs to |

<br>

# PASSWORD_RESET

|  column name | description  | 
|---|---|
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that the password reset key belongs to | 
| RESET_KEY | Large character array used as a key for user to reset their password |
| REQUEST_DATE | Date that the user requested a password reset key |

<br>

# QUESTION 

|  column name | description  | 
|---|---|
| QUESTION_ID | Number ID to uniquely identify question |
| SCHOOL_ID | ID of school from [`SCHOOL`](#SCHOOL) that the question is related to |
| BOOK_ID | ID of book from [`BOOK`](#BOOK) that the question is from |
| QUESTION | Full text of question |
| QUESTION_TYPE | Identifies if question is multiple-choice or free response. 1 if multiple-choice. 0 if free-response |

<br>

# SCHOOL 

|  column name | description  | 
|---|---|
| SCHOOL_ID | Number ID to uniquely identify the school |
| SCHOOL_NAME | Full name of school |

<br>

# STUDY

|  column name | description  | 
|---|---|
| STUDY_ID | Number ID to uniquely identify the study |
| SCHOOL_ID | ID of school from [`SCHOOL`](#SCHOOL) that the study is a part of |
| STUDY_NAME | Full name of study |

<br>

# USER_PROFILE

|  column name | description  | 
|---|---|
| USER_ID | ID to uniquely identify a user |
| EMAIL | Email of a user |
| FIRST_NAME | First name of user |
| LAST_NAME | Last name of user |
| ADMIN | Identifies if user is an admin. 1 if they are an admin. 0 if they are not an admin |
| SCHOOL_ID | ID of school from [`SCHOOL`](#SCHOOL) that the user is a part of |
| CREATED_ON | Date that the user profile was created |
| LAST_LOGIN | Last date that the user logged in |
| PASSWORD | Password for user account |
| STUDY_ID | ID of study from [`STUDY`](#STUDY) that the user is a part of |

<br>

# USER_RESPONE

|  column name | description  | 
|---|---|
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that provided the response | 
| QUESTION_ID | ID of a question from [`QUESTION`](#QUESTION) that the user reponse is related to |
| ANSWER_ID | ID of an answer from [`ANSWER`](#ANSWER) that the user reponse is related to |
| ANSWERED_ON | Date that the user response was recorded |

<br> 

# USER_SESSION

|  column name | description  | 
|---|---|
| SESSION_ID | Number id to identify a user session |
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that the session is for |
| LAST_LOGIN | Date of the most recent time a user was logged in |
| ACTIVE | Identifies if user is actively logged in. 1 if they are logged in. 0 if they are not logged in. |





