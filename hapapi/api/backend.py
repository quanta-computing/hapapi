"""
Haproxy Backend API views

"""
from flask import abort
from flask.views import MethodView
from flask.json import jsonify

from .mixins import HAProxyViewMixin
from .auth import authentication_required

class BackendView(MethodView, HAProxyViewMixin):
    """
    A class to deal with haproxy backends

    """
    URL = '/proxy/<string:proxy>/backend'
    decorators = [authentication_required]


    def list(self, proxy):
        return jsonify({
            'proxy': proxy,
            'backends': self.haproxy.list_backends(proxy),
        })


    def get(self, proxy, name=None):
        if not name:
            return self.list(proxy)
        try:
            backend = self.haproxy.get_backend(proxy, name)
            return jsonify({
                'proxy': proxy,
                'backend': {
                    'name': name,
                    'status': backend.pop('status'),
                    'stats': backend,
                 },
            })
        except KeyError as e:
            raise e
            abort(404)


    def post(self, proxy, name, action):
        try:
            {
                'enable': self.haproxy.enable_backend,
                'disable': self.haproxy.disable_backend,
            }[action](proxy, name)
            return self.get(proxy, name)
        except:
            abort(404)


    def put(self, proxy, name, action):
        return self.post(proxy, name, action)


    @classmethod
    def register(klass, app):
        view = klass.as_view('proxy_backends')
        app.add_url_rule(klass.URL, view_func=view, methods=['GET'])
        app.add_url_rule('{}/<string:name>'.format(klass.URL), view_func=view, methods=['GET'])
        app.add_url_rule('{}/<string:name>/<string:action>'.format(klass.URL), view_func=view, methods=['POST', 'PUT'])
