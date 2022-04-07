"""
app.py

Main launch point for our web server.
"""
from flask import Flask, url_for, Response
import sys
import logging

from edu_storybook.core.config import config
from edu_storybook.api import main
from edu_storybook import admin
from edu_storybook import index
from edu_storybook import login
from edu_storybook import password
from edu_storybook import register
from edu_storybook import story_selection
from edu_storybook import storyboard
from edu_storybook.core.helper import has_no_empty_params
from edu_storybook.core.config import config

from edu_storybook.navbar import make_navbar
from edu_storybook.templates import TEMPLATES

app = Flask('edu_storybook', static_url_path="/static/",
            static_folder="static")

test_client = app.test_client()


app = Flask(__name__, static_url_path="/static/", static_folder="static")

app.register_blueprint(main.api)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('Starting app')

app.register_blueprint(admin.admin)
app.register_blueprint(index.homepage)
app.register_blueprint(login.login)
app.register_blueprint(password.password)
app.register_blueprint(register.register)
app.register_blueprint(story_selection.story_selection)
app.register_blueprint(storyboard.storyboard)


@app.errorhandler(400)
def page_not_found_400(e):
    page_400 = TEMPLATES["_base"].substitute(
        title="400 Error",
        description=str(e),
        body=TEMPLATES['errors']['400'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_400


@app.errorhandler(401)
def page_not_found_401(e):
    page_401 = TEMPLATES["_base"].substitute(
        title="401 Error",
        description=str(e),
        body=TEMPLATES['errors']['401'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_401


@app.errorhandler(403)
def page_not_found_403(e):
    page_403 = TEMPLATES["_base"].substitute(
        title="403 Error",
        description=str(e),
        body=TEMPLATES['errors']['403'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_403


@app.errorhandler(404)
def page_not_found_404(e):
    page_404 = TEMPLATES["_base"].substitute(
        title="404 Error",
        description=str(e),
        body=TEMPLATES['errors']['404'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_404


@app.errorhandler(405)
def page_not_found_405(e):
    page_405 = TEMPLATES["_base"].substitute(
        title="405 Error",
        description=str(e),
        body=TEMPLATES['errors']['405'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_405


@app.errorhandler(500)
def page_not_found_500(e):
    page_500 = TEMPLATES["_base"].substitute(
        title="500 Error",
        description=str(e),
        body=TEMPLATES['errors']['500'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_500


@app.errorhandler(502)
def page_not_found_502(e):
    page_502 = TEMPLATES["_base"].substitute(
        title="502 Error",
        description=str(e),
        body=TEMPLATES['errors']['502'].substitute(
            navbar=make_navbar(None)
        )
    )
    return page_502


def site_map():
    '''
    Generate a dictionary of URLs for this Flask app that have no arguments, and
    do not begin with `/api`. The dictionary is arranged as:

    ```
    {
        url: {
            'endpoint': ...,
            'methods': ...,
            'defaults': ...
        },
        ...
    }
    ```

    Returns: A dictionary arranged as described above.
    '''
    links = {}
    for rule in app.url_map.iter_rules():
        if rule.rule.startswith('/api') or len(rule.arguments) > 0:
            continue
        url = url_for(rule.endpoint, **(rule.defaults or {}))
        links[url] = {
            'endpoint': rule.endpoint,
            'methods': rule.methods,
            'defaults': rule.defaults
        }
    return links


@app.route('/sitemap.txt')
def gen_site_map_txt():
    '''
    Generate the sitemap for this Flask app as a `txt` file.

    Returns: Text file with all routes of the Flask app.
    '''
    links = site_map()
    sitemap = ''
    for rule in links.keys():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if 'GET' in links[rule]['methods']:
            sitemap += config['domain'] + rule + '\n'
    return sitemap, 200, {"Content-Type": "text/plain"}


@app.route('/sitemap.json')
def gen_site_map_json():
    '''
    Generate the sitemap for this Flask app as a `json` file.

    Returns: JSON file with all routes of the Flask app.
    '''
    links = site_map()
    reachable_links = []
    for rule in links.keys():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in links[rule]['methods']:
            reachable_links.append(config['domain'] + rule)
    return {
        "sitemap": reachable_links
    }, 200, {"Content-Type": "application/json"}


@app.route('/sitemap.xml')
def gen_site_map_xml():
    '''
    Generate the sitemap for this Flask app as an `xml` file.

    Returns: XML file with all routes of the Flask app.
    '''
    links = site_map()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for rule in links.keys():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in links[rule]['methods']:
            xml += '\t<url>\n' + \
                f'\t\t<loc>{config["domain"]}{rule}</loc>\n' +\
                f'\t\t<lastmod>{config["last_mod"]}</lastmod>\n' +\
                '\t</url>'
    xml += '</urlset>'
    return xml, 200, {'Content-Type': 'text/xml'}


@app.route('/robots.txt')
def robots_txt() -> Response:
    '''
    Serve the `robots.txt` file from the static folder for SEO.

    Returns: The `robots.txt` as a Flask.Response.
    '''
    return app.send_static_file('robots.txt')


if __name__ == "__main__":
    del test_client
    app.logger.debug(app.url_map)
    app.run(host="0.0.0.0", port="5001", debug=True)
