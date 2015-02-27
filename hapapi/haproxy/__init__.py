"""
This module deals with HAProxy local socket

"""
import socket


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


    def __init__(self, sock_path=DEFAULT_SOCKET):
        self.sock_path = sock_path


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
        sock = self._connect()
        sock.sendall(cmd.encode('ascii'))
        response = b''
        while 42:
            data = sock.recv(self.READ_SIZE)
            response += data
            if len(data) < self.READ_SIZE:
                break
        sock.close()
        return response.decode('ascii')


    def stat(self):
        """
        Executes the stat command and returns the result as a dict

        """
        proxies = {}
        for line in self._command('show stat').splitlines()[1:]:
            line = line.rstrip()
            if not line:
                continue
            proxy, server, *stats = line.split(',')
            if not proxy in proxies:
                proxies[proxy] = {}
            proxies[proxy].update({
                server: dict(zip(self.HAPROXY_STATS, stats))
            })
        return proxies


    def list_proxies(self):
        return list(self.stat().keys())

    def list_backends(self, proxy):
        return list(self.stat()[proxy].keys())

    def get_backend(self, proxy, name):
        return self.stat()[proxy][name]


    def enable_backend(self, proxy, backend):
        return self._command('enable server {}/{}'.format(proxy, backend))

    def disable_backend(self, proxy, backend):
        return self._command('disable server {}/{}'.format(proxy, backend))
