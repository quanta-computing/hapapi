"""
HAproxy views representing a proxy (frontend)

"""
from flask.views import MethodView
from flask.json import jsonify

from .mixins import HAProxyViewMixin
from .auth import authentication_required

class ProxyView(MethodView, HAProxyViewMixin):
    """
    This class represents a haproxy frontend

    """
    URL = '/proxy'
    decorators = [authentication_required]

    def list(self):
        return jsonify({'proxies': self.haproxy.list_proxies()})

    def get(self, name=None):
        if not name:
            return self.list()
        return jsonify({
            'proxy': {
                'name': name,
                'backends': self.haproxy.list_backends(name),
                }
            })

    @classmethod
    def register(klass, app):
        view = klass.as_view('proxies')
        app.add_url_rule(klass.URL, view_func=view, methods=['GET'])
        app.add_url_rule("{}/<string:name>".format(klass.URL), view_func=view, methods=['GET'])
