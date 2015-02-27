"""
Main entry point for hapapi

"""
from flask.json import jsonify

from .. import app
from .. import VERSION

from .proxy import ProxyView
from .backend import BackendView


def root():
    return jsonify({
        'hapapi_version': VERSION,
    })

def register_urls(app):
    """
    Register hapapi URLs

    """
    app.add_url_rule('/', 'index', root)
    ProxyView.register(app)
    BackendView.register(app)


def setup():
    """
    Setup the flask application and return it
    Useful for running it behind a WSGI server

    """
    register_urls(app)
    return app
