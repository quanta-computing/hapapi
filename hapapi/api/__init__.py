"""
Main entry point for hapapi

"""
from flask.json import jsonify


from .root import RootView
from .proxy import ProxyView
from .backend import BackendView


def register_urls(app):
    """
    Register hapapi URLs

    """
    RootView.register(app)
    ProxyView.register(app)
    BackendView.register(app)


def register_error_handlers(app):
    """
    Register custom error handlers to return errors in JSON format

    """
    from werkzeug.exceptions import default_exceptions, HTTPException

    def _json_error(e):
        if isinstance(e, HTTPException):
            code = e.code
        else:
            code = 500
        response = jsonify(error=str(e), code=code)
        response.status_code = code
        return response

    for code in default_exceptions:
        app.error_handler_spec[None][code] = _json_error


def setup(config_file='/etc/haproxy/hapapi.cfg'):
    """
    Setup the flask application and return it
    Useful for running it behind a WSGI server

    """
    from .. import app
    register_urls(app)
    register_error_handlers(app)
    app.config.from_pyfile(config_file)
    return app
