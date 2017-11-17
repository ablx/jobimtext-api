import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestJoBimCount(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_jo_bim_count(self):
        resp = self.api.jo_bim_count('cat', 'NN', 'chase', 'VB', '-subj')
        assert not resp.has_error()
        assert resp.count is not None
