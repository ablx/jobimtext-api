import unittest
from jobimtext import JoBimText
import requests
from pprint import pprint as pp


class TestJoBimText(unittest.TestCase):
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

    def test_holing_trigram(self):
        resp = self.api.holing('I shot the sheriff.', holingtype='trigram')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'trigram'
        assert len(resp.holings) is 5

    def test_jo_similar(self):
        resp = self.api.similar('mouse', 'NN')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'stanford'
        assert resp.method == 'getSimilarTerms'

    def test_jo_similar_trigram(self):
        resp = self.api.similar('mouse', 'NN',holingtype='trigram')
        assert resp.has_error() is False
        assert resp.holingtype_name == 'trigram'
        assert resp.method == 'getSimilarTerms'

    def test_jo_similar_by_score(self):
        resp = self.api.similar('mouse', 'NN').by_score(min_score=50, max_score=200)
        for item in resp:
            assert 50 <= item['score'] < 200

        resp2 = self.api.similar('mouse', 'NN').by_score(min_score=100)
        for item in resp2:
            assert 100 <= item['score']

        resp3 = self.api.similar('mouse', 'NN').by_score(max_score=100)
        for item in resp3:
            assert item['score'] < 100

    def test_count(self):
        resp = self.api.count('mouse', 'NN')
        assert resp.has_error() is False
        assert resp.count > 1000

    def test_count_vb(self):
        resp = self.api.count('program', 'VB')
        assert resp.has_error() is False
        assert resp.count > 10

    def test_senses(self):
        resp = self.api.senses('mouse', 'NN')
        pp(resp._raw)
        assert resp.has_error() is False
        assert len(resp.senses) == 2
        isas_mammal, mammal_sense = resp.isas('mammal')
        assert isas_mammal
        assert mammal_sense.cui == '0'

        has_sense_rat, sense = resp.has_sense('rat', 'NN')
        assert has_sense_rat

        has_sense_program, sense = resp.has_sense('program', 'VB')
        assert not has_sense_program


