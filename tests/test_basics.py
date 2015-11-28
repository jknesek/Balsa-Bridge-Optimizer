import numpy
import unittest
import os
import filecmp
from trussme import truss
from itertools import product

TEST_TRUSS_FILENAME = os.path.join(os.path.dirname(__file__), 'example.trs')

class TestSequenceFunctions(unittest.TestCase):

    def test_iterate_list(self):
        print ""

        l = [2, 3, 4, 5, 6]
        for x in l:
            print x

    def test_iterate_range(self):
        print ""

        l = range(2, 7)
        for x in l:
            print x

    def test_iterate_coordinates(self):

        c1 = list(product([2,3,4], range(2,5)))
        c2 = list(product(range(5,8), range(5,8)))
        c3 = list(product(range(8,12), range(2,5)))

        for j1 in c1:
            for j2 in c2:
                for j3 in c3:
                    print j1, j2, j3


if __name__ == "__main__":
    unittest.main()
