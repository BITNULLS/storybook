# `edu_storybook.api` Module Structure

This Python module is organized in the following manner:

 - [`__init__.py`](__init__.py): Makes this a module.
 - [`main.py`](api.py): Imports of all of the routes of this module from the other scripts.
 - [`index.py`](index.py): All API endpoints that are like `/api/*` (no trailing slash)
    - [Routes](#indexpy)
 - [`admin.py`](admin.py): All API endpoints that begin like `/api/admin/`
    - [Routes](#adminpy)
 - [`password.py`](password.py): All API endpoints that begin like `/api/password/`
    - [Routes](#passwordpy)
 - [`quiz.py`](quiz.py): All API endpoints that begin like `/api/quiz/`
    - [Routes](#quizpy)
 - [`storyboard.py`](storyboard.py): All API endpoints that begin like `/api/storyboard/`
    - [Routes](#storyboardpy)

## Notes

 - All Blueprints in this module should be prefixed with `a_` both in the variable name and the Blueprint name argument. This is just to differentiate the Blueprint namespace between API routes and server-side generated routes.

## index.py

Routes:

 - `/api/`
 - `/api/book`
 - `/api/schools`
 - `/api/login`
 - `/api/logout`
 - `/api/register`

## admin.py

Routes:

 - `/api/admin/book/download`
 - `/api/admin/book/upload`
 - `/api/admin/book/grant`
 - `/api/admin/page`
 - `/api/admin/download/user`
 - `/api/admin/download/action`
 - `/api/admin/get/book`
 - `/api/admin/get/user`

## password.py

 - `/api/password/forgot`
 - `/api/password/reset`

## quiz.py

 - `/api/quiz/submit`

## storyboard.py

 - `/api/storyboard/page/<int:book_id_in>/<int:page_number_in>`
 - `/api/storyboard/action`
