"""
This module contains helper mixins to write API views

"""
from ..haproxy import HAProxy

class HAProxyViewMixin(object):
    """
    A simple class to provide an interface to HAProxy class instance

    """
    def __init__(self):
        self.haproxy = HAProxy()
