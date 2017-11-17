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
        resp = self.api.similar('mouse', 'NN', holingtype='trigram')
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

    def test_jo_count(self):
        resp = self.api.jo_count('mouse', 'NN')
        assert resp.has_error() is False
        assert resp.count > 1000

    def test_bim_count(self):
        resp = self.api.bim_count('mouse', 'NN', 'dobj', holingtype='trigram')
        assert not resp.has_error()

    def test_jo_bim_count(self):
        resp = self.api.jo_bim_count('cat', 'NN', 'chase', 'VB', '-subj')
        assert not resp.has_error()
        assert resp.count is not None

    def test_bim_score(self):
        resp = self.api.bim_score('mouse', 'NN')
        assert not resp.has_error()
        assert len(resp.contexts) > 0

    def test_jo_bim_score(self):
        resp = self.api.jo_bim_score('cat', 'NN', 'chase', 'VB', '-subj')
        assert not resp.has_error()

    def test_isas(self):
        resp = self.api.isas('mouse', 'NN', holingtype='stanford')
        assert not resp.has_error()

    def test_sense_cuis(self):
        resp = self.api.sense_cuis('mouse', 'NN', holingtype='stanford')
        assert not resp.has_error()


    def test_similar_score(self):
        resp = self.api.similar_score('mouse', 'NN', 'cat', 'NN')
        assert resp.score > 70

    def test_count_vb(self):
        resp = self.api.jo_count('program', 'VB')
        assert not resp.has_error()
        assert resp.count > 10

    def test_senses(self):
        resp = self.api.senses('mouse', 'NN')
        assert not resp.has_error()
        assert len(resp.senses) == 2
        isas_mammal, mammal_sense = resp.isas('mammal')
        assert isas_mammal
        assert mammal_sense.cui == '0'

        has_sense_rat, sense = resp.has_sense('rat', 'NN')
        assert has_sense_rat

        has_sense_program, sense = resp.has_sense('program', 'VB')
        assert not has_sense_program
