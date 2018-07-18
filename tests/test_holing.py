import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText
import requests


class TestHoling(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_holing_error(self):
        resp = self.api.holing('foo', holingtype='foo')
        self.assertRaises(requests.HTTPError)
        assert resp.has_error()
        assert resp.error_msg == 'Missing holingtype: foo'

    def test_holing(self):
        resp = self.api.holing('I shot the sheriff.')
        assert resp.has_error() is False
        assert len(resp.holings) is 6

    @unittest.skip("results in timeout since 18.07.2018")
    def test_holing_trigram(self):
        resp = self.api.holing('I shot the sheriff.', holingtype='trigram')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'trigram'
        assert len(resp.holings) is 5
