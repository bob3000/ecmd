import unittest
import urllib.error
import urllib.request
import ecmd.api
from unittest.mock import MagicMock


class TestApi(unittest.TestCase):

    def setUp(self):
        self.request = urllib.request

        self.http_response = MagicMock()
        self.http_response.getheaders = \
            lambda: [("content-type", "application/json")]
        self.http_response.read = \
            lambda: b'{"content": "my content"}'

        attrs = {'urlopen.return_value': self.http_response}
        urllib.request = MagicMock()
        urllib.request.configure_mock(**attrs)

        self.request_Request = urllib.request.Request
        urllib.request.Request = MagicMock()

        self.auth = MagicMock()
        self.auth.authorize_request = lambda x: x

    def test_call(self):
        api = ecmd.api.Api(self.auth, "https://base/url")
        api.call("/servers/list")
        urllib.request.Request.assert_called_with(
            "https://base/url/servers/list",
            headers={'Content-Type': 'text/plain',
                     'Accept': 'application/json'})

    def test_wrong_content_type(self):
        api = ecmd.api.Api(self.auth, "https://base/url")
        self.http_response.getheaders = \
            lambda: [("content-type", "text/html")]
        with self.assertRaises(ecmd.api.ApiException):
            api.call("/servers/list")

    def test_wrong_payload(self):
        api = ecmd.api.Api(self.auth, "https://base/url")
        self.http_response.read = lambda: b'<html></html>'
        with self.assertRaises(ecmd.api.ApiException):
            api.call("/servers/list")

    def test_http_error(self):
        api = ecmd.api.Api(self.auth, "https://base/url")
        attrs = {'urlopen.side_effect':
                 urllib.error.HTTPError(None, None, None, None, None)}
        urllib.request.configure_mock(**attrs)
        with self.assertRaises(ecmd.api.ApiException):
            api.call("/servers/list")

    def tearDown(self):
        urllib.request = self.request
        urllib.request.Request = self.request_Request


class TestAuth(unittest.TestCase):

    def test_authorize_request(self):
        req = MagicMock()
        auth = ecmd.api.Auth("username", "password")
        auth.authorize_request(req)
        req.add_header.assert_called_with('Authorization',
                                          'Basic dXNlcm5hbWU6cGFzc3dvcmQ=')
