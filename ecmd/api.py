import gzip
import json
import urllib.error
import urllib.request


BASE_URL = ""


class Auth():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authorize_request(self, req):
        # TODO: authorize
        return req


class Api():

    default_headers = {
        "Content-Type": "text/plain",
        "Accept": "application/json",
    }

    def __init__(self, auth):
        self.auth = auth

    def call(self, url):
        url = "/".join([BASE_URL, url])
        req = urllib.request.Request(url)
        req = self.auth.authorize_request(req)
        try:
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            raise ApiException(e)
        return self._handle_response(res)

    def _handle_response(self, res):
        headers = {k.lower(): v.lower() for k, v in res.getheaders()}
        if ('application/json' not in headers.get('content-type', "")):
            raise ApiException("content-type is not application/json")
        try:
            try:
                data = json.loads(gzip.decompress(res.read()).decode())
            except OSError:  # response seems not to be gzipped
                data = json.loads(res.read().decode())
        except (TypeError, ValueError):
            raise ApiException("payload is not valid json")
        return ApiResponse(data, res.getcode())


class ApiResponse():

    def __init__(self, payload, code):
        self.payload = payload
        self.code = code


class ApiException(Exception):
    pass
