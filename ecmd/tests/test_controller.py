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
        attrs_server1 = {"uid": "123", "name": "server1", "block:0": "789"}
        attrs_server2 = {"uid": "456", "name": "server2", "block:0": "789"}
        attrs_drive = {"uid": "789", "name": "drive"}
        attrs_server1.update(attrs_gen)
        attrs_server2.update(attrs_gen)
        attrs_drive.update(attrs_gen)
        server1 = MagicMock()
        server2 = MagicMock()
        drive = MagicMock()
        server1.configure_mock(**attrs_server1)
        server2.configure_mock(**attrs_server2)
        drive.configure_mock(**attrs_drive)
        controller.servers = [server1, server2]
        controller.drives = [drive, drive]
        mapping = controller.drive_server_mapping()
        self.assertDictEqual(mapping, dict([('server1', ['drive', 'drive']),
                                            ('server2', ['drive', 'drive'])]))

    def test_exceptions(self):
        self.res.code = 404
        with self.assertRaises(RuntimeError):
            ecmd.controller.Controller("user", "pass", "base_url")
        self.res.code = 200
        error = MagicMock(**{'call.side_effect': ecmd.api.ApiException})
        ecmd.api.Api = MagicMock(return_value=error)
        with self.assertRaises(RuntimeError):
            ecmd.controller.Controller("user", "pass", "base_url")

    def tearDown(self):
        ecmd.api.Api = self.real_api
