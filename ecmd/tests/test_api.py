import gzip
import json
import urllib.error
import urllib.request
import ecmd.lib.auth


BASE_URL = ""


class Api():
    def __init__(self, auth):
        self.auth = auth

    def call(self, url, params=None, post_data=None, headers=None):
        params = params or {}
        post_data = post_data or {}
        headers = headers or {}
        url = self._build_url(url, params)
        if post_data:
            req = urllib.request.Request(
                url, headers=headers, data=post_data.encode(), method="POST")
        else:
            req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            req = self.auth.authorize_request(req)
            res = urllib.request.urlopen(req)
        except (urllib.error.HTTPError, ecmd.lib.auth.AuthException) as e:
            raise ApiException(e)
        return self._handle_response(res)

    def _build_url(self, url, params):
        url = "/".join([BASE_URL, url.strip("/")])
        if params:
            params = sorted(["=".join(map(str, e)) for e in params.items()])
            params = "&".join(params)
            url = "?".join([url, params])
        return url

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
