import base64
import json
import urllib.error
import urllib.request


class Auth():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authorize_request(self, req):
        credentials = "{}:{}".format(self.username, self.password)
        auth = "Basic {}".format(base64.b64encode(credentials.encode()).decode())
        req.add_header("Authorization", auth)
        return req


class Api():

    default_headers = {
        "Content-Type": "text/plain",
        "Accept": "application/json",
    }

    def __init__(self, auth, base_url):
        self.auth = auth
        self.base_url = base_url

    def call(self, url):
        url = "/".join([self.base_url, url.strip("/")])
        req = urllib.request.Request(url, headers=self.default_headers)
        req = self.auth.authorize_request(req)
        try:
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            raise ApiException(e)
        return self._handle_response(res)

    def _handle_response(self, res):
        headers = {k.lower(): v.lower() for k, v in res.getheaders()}
        body = res.read().decode()
        if ('application/json' not in headers.get('content-type', "")):
            raise ApiException("content-type is not application/json")
        try:
            data = json.loads(body)
        except (TypeError, ValueError):
            raise ApiException("payload is not valid json")
        return ApiResponse(data, res.getcode())


class ApiResponse():

    def __init__(self, payload, code):
        self.payload = payload
        self.code = code


class ApiException(Exception):
    pass
