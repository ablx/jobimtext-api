import hammock
import sys
from pprint import pprint as pp
from responses import *

class JoBimText():
    """Original docs: http://ltmaggie.informatik.uni-hamburg.de/jobimtext/jobimviz-web-demo/api-and-demo-documentation/"""


    def __init__(self):
        self.api = hammock.Hammock('http://ltmaggie.informatik.uni-hamburg.de/jobimviz/ws')

    def holing(self, sentence, holingtype='stanford'):
        """
        :param sentence: the sentence
        :param holingtype: stanford or trigram; stanford is default
        :return: HolingResponse
        """
        result = self.api.holing(holingtype).GET(params={'s': sentence})
        return HolingResponse(result.json())


    def similar(self, term, pos, holingtype='stanford'):
        result = self.api.api(holingtype).jo('similar', '{}%23{}'.format(term, pos)).GET()
        return SimilarResponse(result.json())

    def count(self, term, pos, holingtype='stanford'):
        result = self.api.api(holingtype).jo('count', '{}%23{}'.format(term, pos)).GET()
        return CountResponse(result.json())

    def senses(self, term, pos, holingtype='stanford'):
        result = self.api.api(holingtype).jo('senses', '{}%23{}'.format(term, pos)).GET()
        return SensesResponse(result.json())











