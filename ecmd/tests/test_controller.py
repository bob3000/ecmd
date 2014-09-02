import unittest
import ecmd.api
import ecmd.controller
from unittest.mock import MagicMock


class TestController(unittest.TestCase):

    def setUp(self):
        self.real_api = ecmd.api.Api
        self.res = ecmd.api.ApiResponse([{"uuid": "987-654-321"},
                                         {"uuid": "123-456-789"}], 200)
        answer = MagicMock(**{'call.return_value': self.res})
        ecmd.api.Api = MagicMock(return_value=answer)

    def test_drive_server_mapping(self):
        controller = ecmd.controller.Controller("user", "pass", "base_url")
        attrs_gen = {"__gt__": lambda: 0,
                     "__lt__": lambda: 0,
                     "__eq__": lambda: 0,
                     }
        attrs_server = {"uid": "123", "name": "server"}
        attrs_drive = {"uid": "456", "name": "drive"}
        attrs_server.update(attrs_gen)
        attrs_drive.update(attrs_gen)
        server = MagicMock(**attrs_server)
        drive = MagicMock(**attrs_drive)
        controller.servers = [server, server,]
        controller.drives = [drive, drive,]
        controller.drive_server_mapping()

    def tearDown(self):
        ecmd.api.Api = self.real_api
