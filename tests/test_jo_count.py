import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestJoCount(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_jo_count_nn(self):
        resp = self.api.jo_count('mouse', 'NN')

        assert resp.has_error() is False
        assert resp.count > 1000

    def test_count_vb(self):
        resp = self.api.jo_count('program', 'VB')
        assert not resp.has_error()
        assert resp.count > 10
