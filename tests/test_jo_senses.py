import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jobimtextapi.jobimtext import JoBimText


class TestJoSenses(unittest.TestCase):
    def setUp(self):
        self.api = JoBimText()

    def test_isas(self):
        resp = self.api.isas('mouse', 'NN', holingtype='stanford')
        assert not resp.has_error()

    def test_sense_cuis(self):
        resp = self.api.sense_cuis('mouse', 'NN', holingtype='stanford')
        assert not resp.has_error()

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
