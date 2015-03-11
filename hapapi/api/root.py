"""
The root URL for HApAPI

"""
from flask.views import MethodView
from flask.json import jsonify

from .mixins import HAProxyViewMixin
from .auth import authentication_required

class RootView(MethodView, HAProxyViewMixin):
    """
    Root URL class View for HApAPI

    """
    URL = '/'
    decorators = [authentication_required]

    def get(self):
        """
        Root URL

        """
        from .. import VERSION

        info = self.haproxy.info()
        return jsonify({
            'version': VERSION,
            'haproxy': {
                'version': info['Version'],
                'uptime': int(info['Uptime_sec']),
                'current_connections': int(info['CurrConns']),
                'node': info['node'],
            }
        })

    @classmethod
    def register(klass, app):
        """
        Register Root urls to app

        """
        view = klass.as_view('root')
        app.add_url_rule(klass.URL, view_func=view, methods=['GET'])
