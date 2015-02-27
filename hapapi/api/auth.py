"""
Authentication utilities for hapapi

"""
from functools import wraps
from flask import request, abort


def authentication_required(f):
    """
    A view decorator to raise an error if an authentication error occured

    """
    from .. import config

    @wraps(f)
    def _auth(*args, **kwargs):
        if request.headers.get('Authorization', '') != 'Token {}'.format(config.get('token')):
            abort(401)
        return f(*args, **kwargs)
    return _auth
