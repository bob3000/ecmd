# main integration test

## setup

This is a little fake HTTP sever who just serves right answers to the requests.

    >>> import threading
    >>> import re
    >>> import http.server
    >>> class Handler(http.server.BaseHTTPRequestHandler):
    ...     def log_message(self, format, *args):
    ...         return
    ...     def do_GET(s):
    ...         s.send_response(200)
    ...         s.send_header("Content-type", "application/json")
    ...         s.end_headers()
    ...         if s.path.endswith("/list"):
    ...             s.wfile.write(b'[{"uuid": "789"}, {"uuid": "123"}]')
    ...         elif re.search('servers/.*/info', s.path):
    ...             s.wfile.write(b'{"uid": "123", "name": "server1", "block:0": "789"}')
    ...         elif re.search('drives/.*/info', s.path):
    ...             s.wfile.write(b'{"uid": "789", "name": "drive"}')
    ...         else:
    ...             s.wfile.write(b'')

    >>> class Server(threading.Thread):
    ...     def __init__(self):
    ...         threading.Thread.__init__(self)
    ...         self.httpd = http.server.HTTPServer(("", 8000), Handler)
    ...     def stop(self):
    ...         self.httpd.shutdown()
    ...         self.httpd.socket.close()
    ...     def run(self):
    ...         self.httpd.serve_forever()

    >>> deamon = Server()
    >>> deamon.start()

Next we need to fake a few environment variables.

    >>> import os
    >>> real_environ = os.environ
    >>> os.environ = {'EHUUID': '123',
    ...               'EHSECRET': 'secret',
    ...               'EHBASEURL': 'http://localhost:8000'}

## obtaining general information

The `drive` command prints information about available servers the drives they
are using.

    >>> sh("ecmd drives")
    server1: drive drive

There will be an error if the required environment variables are not properly
set.

    >>> os.environ = {}
    >>> sh("ecmd drives")
    Error: the environment variables EHBASEURL EHSECRET EHUUID are not set

## tear down

    >>> os.environ = real_environ
    >>> deamon.stop()
    >>> deamon.join()
