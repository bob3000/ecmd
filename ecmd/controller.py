import ecmd.api
from collections import OrderedDict
from ecmd.resources import Drive, Server


class Controller:

    def __init__(self, username, password, base_url):
        auth = ecmd.api.Auth(username=username, password=password)
        self.api = ecmd.api.Api(auth, base_url)
        self.servers = self._fetch(Server)
        self.drives = self._fetch(Drive)

    def _fetch(self, cls):
        try:
            url = "/{}s/list".format(cls.__name__.lower())
            res = self.api.call(url)
            if 200 != res.code:
                raise RuntimeError("API returned {}".format(res.code))
            return [cls(self.api, uid=uuid['uuid'])
                    for uuid in res.payload]
        except ecmd.api.ApiException as e:
            raise RuntimeError(e)

    def drive_server_mapping(self):
        mapping = {}
        drive_attrs = ("block", "ide", "ata", "scsi",)
        for server in self.servers:
            mapping[server.name] = []
            drive_uids = dict(filter(lambda x: x[0].startswith(drive_attrs),
                              server.__dict__.items())).values()
            for drive in self.drives:
                if drive.uid in drive_uids:
                    mapping[server.name].append(drive.name)
        mapping = {k: sorted(v) for k, v in mapping.items()}
        return OrderedDict(sorted(mapping.items(), key=lambda t: t[0]))
