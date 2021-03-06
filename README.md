# storybook

A motivational storybook that helps students learn.

## Tech

![Visualization of our tech stack](docs/tech-stack.png)

Our web app uses Flask as our server-side framework (generating webpages and serving an API), Oracle as our cloud platform, and CloudFlare as our firewall and DDOS protection. NGINX will act as a WSGI, and run multiple instances of our Flask app for reliability. Our backend will store data in a Oracle Cloud Database.

CloudFlare will cache the frontend, as well as monitor requests to the server for abuse.

This website is entirely server-side generated with some AJAX elements.

## Goals

 - Have a fully functioning web app
 - A user can register, sign in, read a book, answer questions, and sign out
 - An admin can download all useful metadata about a user's progress and performance
 - 100% code coverage on backend API testing
 - Light-footprint on CPU and memory usage

## Directory Structure

 - `edu_storybook/`: Python Flask app to connect the database with the front end.
 - `test_edu_storybook/`: Unit tests for our Flask app.
 - `docs/`: Documentation.

## Requirements

 - `Python >= 3.x`

## Primary Dependencies

 - `cx_Oracle` database driver.
 - `oci` data bucket interface.
 - `pdoc` documentation generator.

## Helpful Links

 - Documentation
    - [Click here to access our prepared documentation for users and developers.](https://docs.google.com/document/d/1CelmwQA7AdvfGEHCVrNK-iNF4JQG2vA7apNBMwooBfk/edit)
    - [Click here to access our formal code documentation.](docs/README.md)
    - [Click here to see generated documentation of our `edu_storybook` module.](docs/pdoc/index.html)
 - [The website, itself.](https://www.edustorybooks.tk/)
 - [Bootstrap v5 Documentation.](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
