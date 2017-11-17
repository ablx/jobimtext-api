import sys
import hammock

from jobimtextapi.responses import *


class JoBimText():
    """Original docs: http://ltmaggie.informatik.uni-hamburg.de/jobimtext/jobimviz-web-demo/api-and-demo-documentation/"""

    def __init__(self, api_url='http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws'):
        self.api = hammock.Hammock(api_url)

    def holing(self, sentence, holingtype='stanford'):
        """
        :param sentence: the sentence
        :param holingtype: stanford or trigram; stanford is default
        :return: HolingResponse
        """
        result = self.api.holing(holingtype).GET(params={'s': sentence})
        return HolingResponse(result.json())

    def similar(self, term, pos='NN', holingtype='stanford'):
        result = self.api.api(holingtype).jo('similar', self._term(term, pos)).GET()
        return SimilarResponse(result.json())

    def jo_count(self, term, pos='NN', holingtype='stanford'):
        result = self.api.api(holingtype).jo('count', self._term(term, pos)).GET()
        return CountResponse(result.json())

    def bim_count(self, term, pos, context, holingtype='stanford'):
        result = self.api.api(holingtype).bim('count', self._context(term, pos, context)).GET()
        return CountResponse(result.json())

    def jo_bim_count(self, term, pos, term2, pos2, context, holingtype='stanford'):
        result = self.api.api(holingtype).jo().bim().count(self._term(term, pos),
                                                           self._context(term2, pos2, context)).GET()
        return CountResponse(result.json())

    def senses(self, term, pos='NN', holingtype='stanford'):
        result = self.api.api(holingtype).jo('senses', self._term(term, pos)).GET()
        return SensesResponse(result.json())

    def isas(self, term, pos='NN', holingtype='stanford'):
        result = self.api.api(holingtype).jo('isas', self._term(term, pos)).GET()
        return SensesResponse(result.json())

    def sense_cuis(self, term, pos='NN', holingtype='stanford'):
        result = self.api.api(holingtype).jo('sense-cuis', self._term(term, pos)).GET()
        return SensesResponse(result.json())

    def similar_score(self, term1, pos1, term2, pos2, holingtype='stanford'):
        result = self.api.api(holingtype).jo('similar-score', self._term(term1, pos1), self._term(term2, pos2)).GET()
        return SimilarScoreResponse(result.json())

    def bim_score(self, term, pos, holingtype='stanford'):
        result = self.api.api(holingtype).jo().bim().score(self._term(term, pos)).GET()
        return ContextScoreResponse(result.json())

    def jo_bim_score(self, term, pos, term2, pos2, context, holingtype='stanford'):
        result = self.api.api(holingtype).jo().bim().score(self._term(term, pos),
                                                           self._context(term2, pos2, context)).GET()
        return SimilarScoreResponse(result.json())

    def _term(self, term, pos):
        return '{}%23{}'.format(term, pos)

    def _context(self, term, pos, context):
        return self._term(self._term(term, pos), context)
