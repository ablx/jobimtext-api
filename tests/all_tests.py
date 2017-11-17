import unittest

from tests.test_bim_count import TestBimCount
from tests.test_bim_score import TestBimScore
from tests.test_holing import TestHoling
from tests.test_jo_bim_count import TestJoBimCount
from tests.test_jo_bim_score import TestJoBimScore
from tests.test_jo_count import TestJoCount
from tests.test_jo_senses import TestJoSenses
from tests.test_jo_similar import TestJoSimilar
from tests.test_jo_similar_score import TestJoSimilarScore

if __name__ == '__main__':
    test_classes_to_run = [TestBimCount, TestBimScore, TestHoling, TestJoBimCount, TestJoBimScore, TestJoCount,
                           TestJoSenses, TestJoSimilar, TestJoSimilarScore]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
