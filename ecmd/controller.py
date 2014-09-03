import concurrent.futures
import ecmd.api
from collections import OrderedDict
from ecmd.resources import Drive, Server


class Controller():

    def __init__(self, username, password, base_url):
        auth = ecmd.api.Auth(username=username, password=password)
        self.api = ecmd.api.Api(auth, base_url)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            try:
                future_servers = executor.submit(self._fetch, Server)
                future_drives = executor.submit(self._fetch, Drive)
                self.servers = future_servers.result()
                self.drives = future_drives.result()
            except ecmd.api.ApiException as e:  # pragma: nocover
                raise RuntimeError(e)

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

    def _eager_load(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            try:
                executor.map(lambda x: x.load(), self.servers)
                executor.map(lambda x: x.load(), self.drives)
            except ecmd.api.ApiException as e:  # pragma: nocover
                raise RuntimeError(e)

    def drive_server_mapping(self):
        mapping = {}
        drive_attrs = ("block", "ide", "ata", "scsi",)
        self._eager_load()
        for server in self.servers:
            mapping[server.name] = []
            drive_uids = dict(filter(lambda x: x[0].startswith(drive_attrs),
                              server.__dict__.items())).values()
            for drive in self.drives:
                if drive.uid in drive_uids:
                    mapping[server.name].append(drive.name)
        mapping = {k: sorted(v) for k, v in mapping.items()}
        return OrderedDict(sorted(mapping.items(), key=lambda t: t[0]))
