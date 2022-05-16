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
 - [`USER_STUDY`](#USER_STUDY)
 - [`BOOK_STUDY`](#BOOK_STUDY)
 - [`LAST_PAGE`](#LAST_PAGE)
 - [`STATIC_PAGE`](#STATIC_PAGE)
 - [`USER_FREE_RESPONSE`](#USER_FREE_RESPONSE)
<br>

# ACTION

This table provides the meta information of a user action on Edu Storybook website

|  column name | description  | 
|---|---|
| USER_ID | ID to identify a user from [`USER_PROFILE`](#USER_PROFILE) |
| ACTION_START | The time that user began the action  |
| ACTION_STOP | The time that the user stopped the action  |
| BOOK_ID | ID of a book from [`BOOK`](#BOOK) that the user enacted the action upon |
| DETAIL_ID | ID of an action detail from [`ACTION_DETAIL`](#ACTION_DETAIL) | \

<br>

# ACTION_DETAIL

This table provides the information of each user action (on Edu Storybook website) in detail

|  column name | description  | 
|---|---|
| DETAIL_ID | Number ID to uniquely identify the detail |
| DETAIL_DESCRIPTION | Text description of the specifics about a user action |
| ACTION_KEY_ID | ID of an action from  [`ACTION_KEY`](#ACTION_KEY) |

<br>

# ACTION_KEY

This table maps the ACTION_KEY_ID (from ACTION_DETAIL Table) to the name of user action

|  column name | description  | 
|---|---|
| ACTION_KEY_ID | Number ID to uniquely identify the action |
| ACTION_NAME | Short hand name of action |

<br>

# ANSWER

This table provides the information about the ideal answer of a question

|  column name | description  | 
|---|---|
| ANSWER_ID | Unique number ID to uniquely identify the answer |
| QUESTION_ID | ID to a question in [`QUESTION`](#QUESTION) that the answer is related to |
| ANSWER | Full text of answer |
| CORRECT | Identifies if an answer to a particular QUESTION_ID is correct. 1 if correct. 0 if they are not correct |
| ANSWER_FEEDBACK | Feedback for an answer. More specifically, this applies to multiple choice options where each
option is an answer and each option has feedback attached to it |

<br>

# BOOK

This table provides the information about the book 

|  column name | description  | 
|---|---|
| BOOK_ID | Unique number ID to uniquely identify the book |
| BOOK_NAME | Full name of book |
| CREATED_ON | Date that the book was added to site |
| DESCRIPTION | Text description of the book |
| PAGE_COUNT | Number of pages in the book |
| FOLDER | Folder that gets created in the cloud bucket for the book |

<br>

# PASSWORD_RESET

This table provides the information about a password reset request being made by the user

|  column name | description  | 
|---|---|
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that the password reset key belongs to | 
| RESET_KEY | Large character array used as a key for user to reset their password |
| REQUEST_DATE | Date that the user requested a password reset key |

<br>

# QUESTION 

This table provides the information about a question being encountered from the book

|  column name | description  | 
|---|---|
| QUESTION_ID | Number ID to uniquely identify question |
| BOOK_ID | ID of book from [`BOOK`](#BOOK) that the question is from |
| QUESTION | Full text of question |
| PAGE_PREV | Page number that is before the question |
| PAGE_NEXT | Page number that is after the question |
| QUESTION_TYPE | Identifies if question is multiple-choice or free response. 1 if multiple-choice. 0 if free-response |

<br>

# SCHOOL 

This table provides the information about a school (more specifically, the name of school)

|  column name | description  | 
|---|---|
| SCHOOL_ID | Number ID to uniquely identify the school |
| SCHOOL_NAME | Full name of school |

<br>

# STUDY

This table provides the information about a study that the user is part of or is involved in the book

|  column name | description  | 
|---|---|
| STUDY_ID | Number ID to uniquely identify the study |
| SCHOOL_ID | ID of school from [`SCHOOL`](#SCHOOL) that the study is a part of |
| STUDY_NAME | Full name of study |
| STUDY_INVITE_CODE | Invite code for a study that a user could join with |

<br>

# USER_PROFILE

This table provides the information about a user upon registering their account on Edu Storybook website

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

<br>

# USER_RESPONSE 

This table provides the information about the user's response on a question 

|  column name | description  | 
|---|---|
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that provided the response | 
| QUESTION_ID | ID of a question from [`QUESTION`](#QUESTION) that the user response is related to |
| ANSWER_ID | ID of an answer from [`ANSWER`](#ANSWER) that the user response is related to |
| ANSWERED_ON | Date that the user response was recorded |

<br> 

# USER_SESSION

This table provides the information of the user's activity status on Edu Storybook website

|  column name | description  | 
|---|---|
| SESSION_ID | Number id to identify a user session |
| USER_ID | ID of a user from [`USER_PROFILE`](#USER_PROFILE) that the session is for |
| LAST_LOGIN | Date of the most recent time a user was logged in |
| ACTIVE | Identifies if user is actively logged in. 1 if they are logged in. 0 if they are not logged in. |

<br>

# USER_STUDY

This table establishes a Many-To-Many relationship between User and Study Tables. One user can be a part of multiple studies. One study can have multiple users involved.

| column name | description |
|---|---|
| USER_ID | ID to uniquely identify a user |
| STUDY_ID | Number ID to uniquely identify the study |

<br>

# BOOK_STUDY

This table establishes a Many-To-Many relationship between Book and Study Tables. One book can have many studies involved. One study can be a part of multiple books.

| column name | description |
|---|---|
| BOOK_ID | Unique number ID to uniquely identify the book |
| STUDY_ID | Number ID to uniquely identify the study |

<br>

# LAST_PAGE

This table provides the information of the last page that a user was accessing on their book

| column name | description |
|---|---|
| USER_ID | ID to uniquely identify a user | 
| BOOK_ID | Unique number ID to uniquely identify the book |
| LAST_PAGE | Last page number that a user was on in their book |
| FURTHEST_READ | Indicates how far a user has gotten in a book (LAST_PAGE <= FURTHEST_READ) |

<br>

# STATIC_PAGE

This table stores static pages (e.g. about page, data disclosure, consent, etc.) that the administrator will want to create, update, and delete

| column name | description |
|---|---|
| PERMANENT | Either 0 or 1 where 0 indicates that the page is not permanent and thus can be safely deleted and 1 indicates that the page is permanent and thus should not be deleted |
| URL | Full URL of the static page |
| NAME | Full name of the static page |
| SHORT_DESCRIPTION | Short description about the static page |
| CREATED_ON | Date when the static page is created on|
| LAST_UPDATE | Date when the static page is last updated on|
| CONTENT | Full content that the static page holds |

<br>

# USER_FREE_RESPONSE

This table will keep track of user free responses (their answers to free response questions)

| column name | description |
|---|---|
| USER_ID | ID to uniquely identify a user |
| QUESTION_ID | Number ID to uniquely identify question |
| RESPONSE | Response provided by the user to the free response question |
| SUBMITTED_ON | Date when the user response to the free response question is submitted |
