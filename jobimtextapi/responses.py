import sys


class BaseResponse():
    """Base response class"""

    def __init__(self, url, data):
        self._raw = data
        self.url = str(url)
        self.error = data['error']
        if not self.has_error():
            self.holingtype = data['holingtype']
            self.holingtype_name = data['holingtype']['name']
        else:
            self.error_msg = self.error['message']

    def has_error(self):
        return self.error is not None


class ResultCountMixin:
    @property
    def result_count(self):
        return len(self._raw['results'])


class MethodMixin:
    @property
    def method(self):
        return self._raw['method']


class HolingResponse(BaseResponse):
    def __init__(self, url, data):
        super(HolingResponse, self).__init__(url, data)
        if not self.has_error():
            self.holings = data['holings']


class SimilarResponse(ResultCountMixin, MethodMixin, BaseResponse):
    def __init__(self, url, data):
        super(SimilarResponse, self).__init__(url, data)
        if not self.has_error():
            self.results = [SimilarResponse.SimilarTerm(e) for e in data['results']]

    def with_score(self, min_score=0, max_score=sys.maxsize):
        """
        Returns all similar terms with similarity >= min score and < max score
        :param min_score: minimum score, inclusive
        :param max_score: max score
        :return:
        """
        return [e for e in self.results if min_score <= e.score < max_score]

    class SimilarTerm:
        def __init__(self, data):
            self._raw = data
            self.context_scores = data['contextScores']
            self.key = data['key']
            self.score = data['score']
            self.term, self.pos = term_and_info(self.key)

        def __repr__(self):
            return '{} ({}) Score: {}'.format(self.term, self.pos, self.score)


class CountResponse(MethodMixin, BaseResponse):
    """Response for Count Operations."""

    def __init__(self, url, data):
        super(CountResponse, self).__init__(url, data)
        self.count = data['result']['count']


class SimilarScoreResponse(MethodMixin, ResultCountMixin, BaseResponse):
    def __init__(self, url, data):
        super(SimilarScoreResponse, self).__init__(url, data)
        self.score = data['result']['score']


class SensesResponse(MethodMixin, ResultCountMixin, BaseResponse):
    class Sense():
        def __init__(self, data):
            self.cui = data['cui']
            self.isas = data['isas']
            self.senses = data['senses']

    def __init__(self, url, data):
        super(SensesResponse, self).__init__(url, data)
        self.senses = [SensesResponse.Sense(s) for s in data['result']]

    def isas(self, term):
        for sense in self.senses:
            for s in sense.isas:
                word = s.split(':')
                if word[0].lower() == term.lower():
                    return True, sense
        return False, None

    def has_sense(self, sense, pos=None):
        for _sense in self.senses:
            for s in _sense.senses:
                val, p = term_and_info(s)
                if val == sense and p == pos:
                    return True, sense
        return False, None


class ContextScoreResponse(MethodMixin, ResultCountMixin, BaseResponse):
    class Context():
        def __init__(self, data):
            self.count = data['count']
            self.key = data['key']
            self.score = data['score']

    def __init__(self, url, data):
        super(ContextScoreResponse, self).__init__(url, data)
        self.contexts = [ContextScoreResponse.Context(d) for d in data['results']]


def split_on_hash(word):
    if '#' in word:
        return word.split('#')
    else:
        return word


def term_and_info(string):
    if '#' in string:
        return string.split('#')
    return string, None
