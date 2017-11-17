import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestJoSimilarScore(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_similar_score(self):
        resp = self.api.similar_score('mouse', 'NN', 'cat', 'NN')
        assert resp.score > 70
