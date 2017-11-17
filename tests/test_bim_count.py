import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestBimCount(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_bim_count(self):
        resp = self.api.bim_count('mouse', 'NN', 'dobj', holingtype='trigram')
        assert not resp.has_error()
