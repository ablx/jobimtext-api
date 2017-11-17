import sys


class BaseResponse():
    def __init__(self, data):
        self._raw = data
        self.error = data['error']
        if not self.has_error():
            self.holingtype = data['holingtype']
            self.holingtype_name = data['holingtype']['name']
        else:
            self.error_msg = self.error['message']

    def has_error(self):
        return self.error is not None


class MethodResponse(BaseResponse):
    def __init__(self, data):
        super(MethodResponse, self).__init__(data)
        self.method = data['method']


class HolingResponse(BaseResponse):
    def __init__(self, data):
        super(HolingResponse, self).__init__(data)
        if not self.has_error():
            self.holings = data['holings']


class SimilarResponse(MethodResponse):
    def __init__(self, data):
        super(SimilarResponse, self).__init__(data)
        if not self.has_error():
            self.results = data['results']

    def by_score(self, min_score=0, max_score=sys.maxsize):
        return [e for e in self.results if min_score <= e['score'] < max_score]


class CountResponse(MethodResponse):
    def __init__(self, data):
        super(CountResponse, self).__init__(data)
        self.count = data['result']['count']


class SimilarScoreResponse(MethodResponse):
    def __init__(self, data):
        super(SimilarScoreResponse, self).__init__(data)
        self.score = data['result']['score']


class SensesResponse(MethodResponse):
    class Sense():
        def __init__(self, data):
            self.cui = data['cui']
            self.isas = data['isas']
            self.senses = data['senses']

    def __init__(self, data):
        super(SensesResponse, self).__init__(data)
        self.senses = [SensesResponse.Sense(s) for s in data['result']]

    def isas(self, term):
        for sense in self.senses:
            for s in sense.isas:
                word = s.split(':')
                if word[0].lower() == term.lower():
                    return True, sense
        return False, None

    def has_sense(self, sense, pos='NN'):
        for _sense in self.senses:
            for s in _sense.senses:
                val, p = s.split('#')
                if val.lower() == sense.lower() and p.lower() == pos.lower():
                    return True, sense
        return False, None


class ContextScoreResponse(MethodResponse):
    class Context():
        def __init__(self, data):
            self.count = data['count']
            self.key = data['key']
            self.score = data['score']

    def __init__(self, data):
        super(ContextScoreResponse, self).__init__(data)
        self.contexts = [ContextScoreResponse.Context(d) for d in data['results']]
