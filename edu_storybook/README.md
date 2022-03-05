# `edu_storybook` Module Structure

This Python module is organized in the following manner:

 - [`api/`](api/README.md): Contains the `edu_storybook.api` module, which holds all the `/api/` endpoints, split by responsbility (usually endpoint prefix).
 - [`core/`](core/README.md): Contains the `edu_storybook.core` module, which holds the critical code that is reused everywhere (database and bucket access, loading in config, helper functions, authentication, and more).
 - [`sql/`](sql/): Prepared SQL statements that are used for basic queries, and initializing the database.
 - [`templates/`](templates/): This folder contains the templates that are generated for the user.
 - [`app.py`](#apppy): The main launch point of the server.
 - [`admin.py`](#adminpy): Contains all of the routes corresponding to admin, beginning with `/admin/`.
 - [`index.py`](#indexpy): Contains all of the routes corresponding to the route of the website, `/`. 
 - [`login.py`](#loginpy): Only the `/login` endpoint.
 - [`password.py`](#passwordpy): Password forget and reset endpoints.
 - [`register.py`](#registerpy): Only the `/register` endpoint.
 - [`story_selection.py`](#storyselectionpy): Only the `/books` endpoint.
 - [`storyboard.py`](#storyboardpy): Several endpoints relating to the storyboard viewer.

## Notes

**Rule of thumb:** All `edu_storybook/*.py` files (except for `app.py`) corresponds to an HTML file in the `templates/` directory, or a directory in the `templates/` directory. For example, `admin.py` corresponds to the `admin/` directory, which contains HTML templates. `index.py` only corresponds to `index.py`.

**Templating note:** We are using the Python built-in `string.Template` module to template the webpages. There are more complex templating engines available, but we believe philosophically that all code should be in Python scripts. Code written into templates (with other templating engines) are not easily understandable (different syntax) and not directly testable. To keep things simple, our templates will only allow HTML to be directly injected into the specified places. Python's `string.Template` forces a "Russian-stacking doll" approach to building a webpage, and every template that specifies a parameter must be filled in. If `x` parameter is in a template, it must be filled in by the Template.

**Templating Delimiter:** Our template delimeter is `~`. The default `$` of `string.Template` conflicts with JQuery's `$` JavaScript identifier/alias.

**Styling:** Single quote (`'`) strings should be used everywhere possible.

**Tabs vs Spaces:** 4 spaces.

---

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