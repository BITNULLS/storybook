# `edu_storybook` Module Structure

This Python module is organized in the following manner:

 - [`core/`](core/README.md): Contains the `edu_storybook.core` module, which holds the critical code that is reused everywhere (database and bucket access, loading in config, helper functions, and more).
 - `templates/`: This folder contains the templates that are generated for the user.
 - [`app.py`](#apppy): The main launch point of the server.
 - [`admin.py`](#adminpy): Contains all of the routes corresponding to admin, beginning with `/admin/`.
 - [`index.py`](#indexpy): Contains all of the routes corresponding to the route of the website, `/`. 
 - [`login.py`](#loginpy): Only the `/login` endpoint.
 - [`password.py`](#passwordpy): Password forget and reset endpoints.
 - [`register.py`](#registerpy): Only the `/register` endpoint.
 - [`story_selection.py`](#storyselectionpy): Only the `/books` endpoint.
 - [`storyboard.py`](#storyboardpy): Several endpoints relating to the storyboard viewer.

Rule of thumb: All `edu_storybook/*.py` files (except for `app.py`) corresponds to an HTML file in the `templates/` directory, or a directory in the `templates/` directory. For example, `admin.py` corresponds to the `admin/` directory, which contains HTML templates. `index.py` only corresponds to `index.py`.

## app.py

The controller of the server. Only launches Flask and calls other initialization scripts.

## admin.py

...

## index.py

...

## login.py

Routes: 
 - `login/`

Purpose: To allow the user to login to the website. Handles giving JWT session cookie to user.

## password.py

...

## register.py

...

## story_selection.py

...

## storyboard.py

...
