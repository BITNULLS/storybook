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
 - [`navbar.py`](navbar.py): Generate the navbar for many pages.
 - [`password.py`](#passwordpy): Password forget and reset endpoints.
 - [`register.py`](#registerpy): Only the `/register` endpoint.
 - [`story_selection.py`](#storyselectionpy): Only the `/books` endpoint.
 - [`storyboard.py`](#storyboardpy): Several endpoints relating to the storyboard viewer.

## All Endpoints

```
 <Rule '/api/admin/download/action' (OPTIONS, POST) -> api.a_admin.admin_download_action_data>,
 <Rule '/api/admin/download/user' (OPTIONS, POST) -> api.a_admin.admin_download_user_data>,
 <Rule '/api/admin/book/download' (OPTIONS, POST) -> api.a_admin.admin_download_book>,
 <Rule '/api/admin/book/upload' (OPTIONS, POST) -> api.a_admin.admin_book_upload>,
 <Rule '/api/admin/book/grant' (OPTIONS, POST) -> api.a_admin.admin_add_book_to_study>,
 <Rule '/api/admin/get/user' (HEAD, OPTIONS, GET) -> api.a_admin.admin_get_users>,
 <Rule '/api/admin/get/book' (HEAD, OPTIONS, GET) -> api.a_admin.admin_get_books>,
 <Rule '/api/storyboard/action' (OPTIONS, POST) -> api.a_storyboard.storyboard_save_user_action>,
 <Rule '/api/password/forgot' (OPTIONS, POST) -> api.a_password.password_forgot>,
 <Rule '/api/password/reset' (OPTIONS, POST) -> api.a_password.password_reset>,
 <Rule '/api/admin/page' (GET, HEAD, DELETE, PUT, OPTIONS, POST) -> api.a_admin.admin_page_handler>,
 <Rule '/api/quiz/submit' (OPTIONS, POST) -> api.a_quiz.quiz_submit_answer>,
 <Rule '/password/forgot' (HEAD, OPTIONS, GET) -> password.gen_password_forgot>,
 <Rule '/password/reset' (HEAD, OPTIONS, GET) -> password.gen_password_reset>,
 <Rule '/admin/study_manager' (HEAD, OPTIONS, GET) -> admin.gen_admin_study_manager>,
 <Rule '/admin/book_manager' (HEAD, OPTIONS, GET) -> admin.gen_admin_book_mananger>,
 <Rule '/admin/upload_book' (HEAD, OPTIONS, GET) -> admin.gen_admin_upload_book>,
 <Rule '/admin/edit_book' (HEAD, OPTIONS, GET) -> admin.gen_admin_edit_book>,
 <Rule '/api/register' (OPTIONS, POST) -> api.a_index.register>,
 <Rule '/api/schools' (HEAD, OPTIONS, GET) -> api.a_index.get_schools>,
 <Rule '/api/logout' (OPTIONS, POST) -> api.a_index.logout>,
 <Rule '/api/login' (OPTIONS, POST) -> api.a_index.login>,
 <Rule '/api/book' (HEAD, OPTIONS, GET) -> api.a_index.get_users_books>,
 <Rule '/register' (HEAD, OPTIONS, GET) -> register.gen_register>,
 <Rule '/admin/' (HEAD, OPTIONS, GET) -> admin.gen_admin_index>,
 <Rule '/login' (HEAD, OPTIONS, GET) -> login.gen_login>,
 <Rule '/books' (HEAD, OPTIONS, GET) -> story_selection.gen_books>,
 <Rule '/api/' (HEAD, OPTIONS, GET) -> api.a_index.api_index>,
 <Rule '/' (HEAD, OPTIONS, GET) -> homepage.gen_index>,
 <Rule '/api/storyboard/page/<book_id_in>/<page_number_in>' (HEAD, OPTIONS, GET) -> api.a_storyboard.storyboard_get_page>,
 <Rule '/storyboard/pagecount/<book_id_in>' (HEAD, OPTIONS, GET) -> api.a_storyboard.storyboard_get_pagecount>,
 <Rule '/storyboard/<book_id_in>/<page_number_in>' (HEAD, OPTIONS, GET) -> storyboard.gen_storyboard_page>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>]
```

## Developer Notes

**Rule of thumb:** All `edu_storybook/*.py` files (except for `app.py`) corresponds to an HTML file in the `templates/` directory, or a directory in the `templates/` directory. For example, `admin.py` corresponds to the `admin/` directory, which contains HTML templates. `index.py` only corresponds to `index.py`.

**Templating note:** We are using the Python built-in `string.Template` module to template the webpages. There are more complex templating engines available, but we believe philosophically that all code should be in Python scripts. Code written into templates (with other templating engines) are not easily understandable (different syntax) and not directly testable. To keep things simple, our templates will only allow HTML to be directly injected into the specified places. Python's `string.Template` forces a "Russian-stacking doll" approach to building a webpage, and every template that specifies a parameter must be filled in. If `x` parameter is in a template, it must be filled in by the Template.

**Templating Delimiter:** Our template delimeter is `~`. The default `$` of `string.Template` conflicts with JQuery's `$` JavaScript identifier/alias.

**Styling:** Single quote (`'`) strings should be used everywhere possible.

**Tabs vs Spaces:** 4 spaces.

**Column Character Limit (Print Margin):** 80 characters.

## Common Acronyms

 - **SSG**: Server-side generated (pages); templated pages
 - **DB**: Database
 - **DBA**: Database Administrator

---

## app.py

The controller of the server. Only launches Flask and calls other initialization scripts.

## admin.py

Generates all of the admin (`/admin/*`) pages.

## index.py

Generates the `/` homepage.

## login.py

Generates only the `/login` page.

## password.py

Generates the `/password/*` pages.

## register.py

Generates only the `/register` page.

## story_selection.py

Generates only the `/books` page.

## storyboard.py

Generates only the storyboard viewer page.
