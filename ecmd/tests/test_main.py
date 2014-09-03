import unittest
import argparse
import os
import sys
import ecmd.controller
from unittest.mock import MagicMock, patch


def namespace(contents):
    n = argparse.Namespace()
    n.__dict__.update(contents)
    return n


class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.real_controller = ecmd.controller
        ecmd.controller = MagicMock()
        ecmd.__main__.controller = MagicMock()
        self.real_exit = sys.exit
        sys.exit = MagicMock()
        self.real_stderr = sys.stderr
        sys.stderr = MagicMock()
        self.real_environ = os.environ
        os.environ = MagicMock(return_value={"EHUUID": "123",
                                             "EHSECRET": "secret",
                                             "EHBASEURL": "http://url"})

    def test_args_drives(self):
        result = ecmd.__main__.parse_args(['drives'])
        result = filter(lambda x: x[0] != 'func', result.__dict__.items())
        self.assertDictEqual(dict(result), {'command': 'drives'})

    @patch('sys.stdout')
    def test_commands(self, stdout):
        controller = MagicMock(**{'drive_server_mapping.return_value':
                                      {"server": ["drive1", "drive2"]}})
        ecmd.__main__.controller = controller
        ecmd.__main__.commands(namespace({'command': 'drives'}))
        ecmd.__main__.controller= MagicMock(
            **{'drive_server_mapping.side_effect': RuntimeError})
        sys.exit.mock_reset
        ecmd.__main__.commands(namespace({'command': 'drives'}))
        self.assertTrue(sys.exit.called)

    @patch('ecmd.__main__.parse_args')
    def test_main(self, parse_args):
        parse_args.return_value = namespace({'func': lambda x: x})
        ecmd.__main__.main()
        self.assertTrue(ecmd.controller.Controller.called)
        ecmd.__main__.controller.mock_reset()
        os.environ = MagicMock(return_value={"EHBASEURL": "http://url"})
        self.assertTrue(sys.exit.called)
        sys.exit.mock_reset

    def tearDown(self):
        ecmd.controller = self.real_controller
        sys.exit = self.real_exit
        sys.stderr = self.real_stderr
        os.environ = self.real_environ
