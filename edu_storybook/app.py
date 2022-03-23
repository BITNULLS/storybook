"""
app.py

Main launch point for our web server.
"""
import sys

from flask import Flask, url_for, Response

from edu_storybook.core.config import config
from edu_storybook.api import main
import admin
import index
import login
import password
import register
import story_selection
import storyboard
from edu_storybook.core.helper import has_no_empty_params
from edu_storybook.core.config import config

import logging

app = Flask('edu_storybook', static_url_path="/static/", static_folder="static")

test_client = app.test_client()

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('Starting app')

app.register_blueprint(main.api)
app.register_blueprint(admin.admin)
app.register_blueprint(index.homepage)
app.register_blueprint(login.login)
app.register_blueprint(password.password)
app.register_blueprint(register.register)
app.register_blueprint(story_selection.story_selection)
app.register_blueprint(storyboard.storyboard)


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
