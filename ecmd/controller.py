import sys
import ecmd.lib.api
import ecmd.lib.auth
import ecmd.resources


class Controller:

    def __init__(self):
        auth = ecmd.lib.auth.Auth()
        self.api = ecmd.lib.api.Api(auth)
        self.servers = _load("server")
        self.drives = _load("drive")

    def _load(self, res_type):
        try:
            res = self.api.call("/{}s/list".format(res_type))

        except ecmd.lib.api.ApiException as e:
            raise RuntimeError(e)
