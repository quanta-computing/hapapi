"""
Authentication utilities for hapapi

"""
from functools import wraps
from flask import request, abort


def authentication_required(f):
    """
    A view decorator to raise an error if an authentication error occured

    """
    from .. import app

    @wraps(f)
    def _auth(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token:
            abort(401)
        if token != 'Token {}'.format(app.config['AUTH_TOKEN']):
            abort(403)
        return f(*args, **kwargs)
    return _auth
