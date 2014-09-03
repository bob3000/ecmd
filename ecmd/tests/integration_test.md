# main integration test

## setup

    >>> import threading
    >>> import re
    >>> import http.server
    >>> class Handler(http.server.BaseHTTPRequestHandler):
    ...     def do_GET(s):
    ...         s.send_response(200)
    ...         s.send_header("Content-type", "application/json")
    ...         s.end_headers()
    ...         if s.path.endswith("/list"):
    ...             s.wfile.write(b'[{"uuid": "987-654-321"}, {"uuid": "123-456-789"}]')
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

The `info` command prints general information about available servers and
belonging drives.

    >>> sh("ecmd drives")

## tear down

    >>> os.environ = real_environ
