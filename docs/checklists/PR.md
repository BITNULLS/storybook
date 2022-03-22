# Pull Request Submission Checklist

Before submitting a Pull Request (PR)

- Make sure that you have wrote thorough Python documentation of any new functions that you write
    - [Use the example pydoc string example below as a reference.](#example-pydoc-string)
- If you edited a file in a directory, check the `README.md`s in that directory, and all parent directories as necessary.  If you change something that makes the current documentation different/incorrect, updates to the READMEs need to be reflected, appropriately
    - e.g. if editing `folder_a/b/c.py`; update `folder_a/b/README.md`, `folder_a/README.md` and `README.md` (the repository's top-level README).
- Styling
    - This should be enforced by `.vscode/settings.json`, but
    - 4 spaces over tabs
    - Follow [PEP8](https://www.google.com/search?client=safari&rls=en&q=python+pep8&ie=UTF-8&oe=UTF-8)
    - Basically: `snake_case` for variables, functions, and methods, `CapsCase` for classes.
- Security
    - If writing a new endpoint.
    - Ask: Who should be able to access this endpoint? Everyone, logged in users, or administrators?
    - Make sure to use the `validate_login` function. Look for examples in `edu_storybook.api.admin`.
- Test
    - **When writing a new endpoint**: Use Postman/curl to send a test request to an endpoint. Screenshot it, and include it in the PR to prove it works.
    - **When changing UI elements**: Please include a screenshot of the effects of changing a template/HTML/CSS. Optionally (and appreciated) is to include a before screenshot.


## Summarized Checklist

 - Write Python documentation.
 - Update READMEs, recursively up the parent folders.
 - Follow Python stlying (when in doubt, check surrounding code for context or clues).
 - Evaluate how much privilege a user should have to access an endpoint, and check it.
 - Test, and document your testing.

## Example Pydoc String

Here's an example pydoc string for a regular function.

```
def my_cool_function(argument: str) -> str:
    '''
    This function does a thing.

    Args:
     - argument: A cool argument.

    Returns: Useful string.
    '''
    some_stuff()
    ...
    return 'e'
```

For any function in `edu_storybook.api`, follow this pydoc string:

```
@blueprint.route('/cool/route', methods=['POST'])
def my_cool_route():
    '''
    Gets user a refreshing cold glass of soda.

    Expects:
     - age: The user's age as an integer.

    Fails:
     - `1`: Non-int value for `age`
     - `2`: Age too low.
     - `3`: Age too high.

    Returns: Coupon for a free soda pop.
    '''
```

Since we're using `pdoc` to generate documentation, [it supports Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
