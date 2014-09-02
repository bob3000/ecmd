import unittest
import ecmd.api
import ecmd.resources
from unittest.mock import MagicMock


class TestResource(unittest.TestCase):

    def setUp(self):
        self.api = MagicMock()
        self.res = ecmd.api.ApiResponse({"name": "number9"}, 200)
        self.api.configure_mock(**{'call.return_value': self.res})

    def test_load(self):
        drive = ecmd.resources.Drive(self.api, '123-456-789')
        self.assertEqual(drive.name, "number9")

    def test_attr_exception(self):
        self.api.configure_mock(**{'call.side_effect': ecmd.api.ApiException})
        with self.assertRaises(ecmd.resources.ResourceException):
            server = ecmd.resources.Server(self.api, '987-654-321')
            server.name

    def test_wrong_response_code(self):
        self.res.code = 404
        with self.assertRaises(ecmd.resources.ResourceException):
            server = ecmd.resources.Server(self.api, '987-654-321')
            server.name
