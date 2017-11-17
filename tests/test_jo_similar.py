import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestJoSimilar(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_jo_similar(self):
        resp = self.api.similar('mouse', 'NN')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'stanford'
        assert resp.method == 'getSimilarTerms'
        assert resp.result_count > 10

    def test_jo_similar_better(self):
        resp = self.api.similar('better', pos=None, url_params={'numberOfEntries': 1000}, holingtype='trigram')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'trigram'
        assert resp.method == 'getSimilarTerms'

    def test_jo_similar_trigram(self):
        resp = self.api.similar('mouse', 'NN', holingtype='trigram')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'trigram'
        assert resp.method == 'getSimilarTerms'

    def test_jo_similar_by_score(self):
        resp = self.api.similar('mouse', 'NN').with_score(min_score=50, max_score=200)
        for item in resp:
            assert 50 <= item.score < 200

        resp2 = self.api.similar('mouse', 'NN').with_score(min_score=100)
        for item in resp2:
            assert 100 <= item.score

        resp3 = self.api.similar('mouse', 'NN').with_score(max_score=100)
        for item in resp3:
            assert item.score < 100
