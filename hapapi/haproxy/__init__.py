"""
This module deals with HAProxy local socket

"""
import socket

from werkzeug.exceptions import HTTPException


class HAProxyError(HTTPException):
    """
    Exception class to deal with HAproxy socket errors

    """

    def __init__(self, message, code=500):
        self.code = 500
        self.description = message

    def __str__(self):
        return str(self.description)


class HAProxy(object):
    """
    This class interacts with the HAProxy stats socket

    """
    DEFAULT_SOCKET = '/tmp/haproxy.sock'
    READ_SIZE = 42
    HAPROXY_STATS = [
        'qcur', 'qmax', 'scur', 'smax', 'slim', 'stot', 'bin', 'bout',
        'dreq', 'dresp', 'ereq', 'econ', 'eresp', 'wretr', 'wredis', 'status',
        'weight', 'act', 'bck', 'chkfail', 'chkdown', 'lastchg', 'downtime',
        'qlimit', 'pid', 'iid', 'sid', 'throttle', 'lbtot', 'tracked', 'type',
        'rate', 'rate_lim', 'rate_max', 'check_status', 'check_code',
        'check_duration', 'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx',
        'hrsp_5xx', 'hrsp_other', 'hanafail', 'req_rate', 'req_rate_max',
        'req_tot', 'cli_abrt', 'srv_abrt', 'comp_in', 'comp_out', 'comp_byp',
        'comp_rsp', 'lastsess', 'last_chk', 'last_agt', 'qtime', 'ctime',
        'rtime', 'ttime'
    ]
    INTERNAL_BACKEND_NAMES = ['BACKEND', 'FRONTEND']

    def __init__(self):
        from .. import app
        self.sock_path = app.config.get('HAPROXY_SOCKET', self.DEFAULT_SOCKET)


    def _connect(self):
        """
        Connects to the haproxy UNIX socket

        """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(self.sock_path)
        return sock


    def _command(self, cmd):
        """
        Sends a command and reads the reply

        """
        cmd = cmd.rstrip() + '\n'
        try:
            sock = self._connect()
            sock.sendall(cmd.encode('ascii'))
        except:
            raise HAProxyError('Cannot connect to HAproxy local socket. Is HAproxy running ?')
        response = b''
        while 42:
            data = sock.recv(self.READ_SIZE)
            response += data
            if len(data) < self.READ_SIZE:
                break
        sock.close()
        return response.decode('ascii')


    def info(self):
        """
        Returns the informations related to HAproxy status as a dict

        """
        return dict(map(
            lambda l: tuple(map(lambda v: v.rstrip(), l.split(': '))),
            self._command('show info').splitlines()[:-1]
        ))


    def stat(self):
        """
        Executes the stat command and returns the result as a dict

        """
        def _to_int_safe(value):
            """
            Try to converts the value to an integer but returns the value as is
            if it is not possible

            """
            try:
                return int(value)
            except ValueError as e:
                return value

        proxies = {}
        for line in self._command('show stat').splitlines()[1:]:
            line = line.rstrip()
            if not line:
                continue
            proxy, server, *stats = line.split(',')
            stats = dict(zip(self.HAPROXY_STATS, map(_to_int_safe, stats)))
            if not proxy in proxies:
                proxies[proxy] = {
                    'stats': {},
                    'backends': {},
                }
            if server in self.INTERNAL_BACKEND_NAMES:
                key = 'stats'
            else:
                key = 'backends'
            proxies[proxy][key].update({
                server: stats,
            })
        return proxies


    def list_proxies(self):
        return list(self.stat().keys())

    def list_backends(self, proxy):
        return list(self.stat()[proxy]['backends'].keys())

    def get_backend(self, proxy, name):
        return self.stat()[proxy]['backends'][name]

    def get_proxy(self, proxy):
        return self.stat()[proxy]


    def enable_backend(self, proxy, backend):
        return self._command('enable server {}/{}'.format(proxy, backend))

    def disable_backend(self, proxy, backend):
        return self._command('disable server {}/{}'.format(proxy, backend))
