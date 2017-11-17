import sys
import hammock

from jobimtextapi.responses import *


class JoBimText():
    """Original docs: http://ltmaggie.informatik.uni-hamburg.de/jobimtext/jobimviz-web-demo/api-and-demo-documentation/"""

    def __init__(self, api_url='http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws'):
        self.api = hammock.Hammock(api_url)

    def holing(self, sentence, url_params={}, holingtype='stanford'):
        """
        :param sentence: the sentence
        :param holingtype: stanford or trigram; stanford is default
        :return: HolingResponse
        """
        url = self.api.holing(holingtype)
        result = url.GET(params={'s': sentence})
        return HolingResponse(url, result.json())

    def similar(self, term, pos=None, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('similar', self._term(term, pos))
        result = url.GET(params=url_params)
        return SimilarResponse(url, result.json())

    def jo_count(self, term, pos=None,  url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('count', self._term(term, pos))
        result = url.GET(params=url_params)
        return CountResponse(url, result.json())

    def bim_count(self, term, pos, context, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).bim('count', self._context(term, pos, context))
        result = url.GET(params=url_params)
        return CountResponse(url, result.json())

    def jo_bim_count(self, term, pos, term2, pos2, context, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo().bim().count(self._term(term, pos), self._context(term2, pos2, context))
        result = url.GET(params=url_params)
        return CountResponse(url, result.json())

    def senses(self, term, pos=None, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('senses', self._term(term, pos))
        result = url.GET(params=url_params)
        return SensesResponse(url, result.json())

    def isas(self, term, pos=None, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('isas', self._term(term, pos))
        result = url.GET(params=url_params)
        return SensesResponse(url, result.json())

    def sense_cuis(self, term, pos=None, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('sense-cuis', self._term(term, pos))
        result = url.GET(params=url_params)
        return SensesResponse(url, result.json())

    def similar_score(self, term1, pos1, term2, pos2, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo('similar-score', self._term(term1, pos1), self._term(term2, pos2))
        result = url.GET(params=url_params)
        return SimilarScoreResponse(url, result.json())

    def bim_score(self, term, pos=None, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo().bim().score(self._term(term, pos))
        result = url.GET(params=url_params)
        return ContextScoreResponse(url, result.json())

    def jo_bim_score(self, term, pos, term2, pos2, context, url_params={}, holingtype='stanford'):
        url = self.api.api(holingtype).jo().bim().score(self._term(term, pos), self._context(term2, pos2, context))
        result = url.GET(params=url_params)
        return SimilarScoreResponse(url, result.json())

    def _term(self, term, pos):
        if pos is None:
            return term
        return '{}%23{}'.format(term, pos)

    def _context(self, term, pos, context):
        return self._term(self._term(term, pos), context)
