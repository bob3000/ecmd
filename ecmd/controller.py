import ecmd.lib.api
import ecmd.resources


class Controller:

    def __init__(self):
        def _load(self, res_type):
            try:
                res = self.api.call("/{}s/list".format(res_type))
                return res  ## make a list of data objects
            except ecmd.lib.api.ApiException as e:
                raise RuntimeError(e)

        auth = ecmd.lib.api.Auth(username=None, password=None)
        self.api = ecmd.lib.api.Api(auth)
        self.servers = self._load("server")
        self.drives = self._load("drive")

    def info(self):
        mapping = {}
        for drive in self.drives:
            for server in drive.claimed:
                if server not in mapping:
                    mapping.update({server: []})
                mapping[server].append(drive)
        return mapping
