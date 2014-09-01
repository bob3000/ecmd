# main integration test

## preparation

The `urllib.request.urlopen` function needs to be patched in order to avoid
sending real HTTP request against some API.

    >>> import urllib.request
    >>> from unittest.mock import MagicMock
    >>> urllib.request.urlopen = MagicMock()

The mock needs to return an object which offers all the used methods from the
`http.client.HTTPResponse` class for the whole program to work.

    >>> import http.client
    >>> fake_response_methods = {
    ...     "getheaders.return_value": [("content-type", "application/json")],
    ...     "read.return_value": b'{"title": "a title", "body": "msg body"}',
    ...     "getcode.return_value": 200,
    ...     }

    >>> fake_response = MagicMock(spec_set=http.client.HTTPResponse)
    >>> urllib.request.urlopen.return_value = fake_response
    >>> fake_response.configure_mock(**fake_response_methods)

## obtaining general information

The `info` command prints general information about available servers and
belonging drives.

    >>> sh("ecmd info")
