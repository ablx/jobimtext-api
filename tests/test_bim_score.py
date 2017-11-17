import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestBimScore(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_bim_score(self):
        resp = self.api.bim_score('mouse', 'NN')
        assert not resp.has_error()
        assert len(resp.contexts) > 0
