import numpy
import unittest
import os
import filecmp
from trussme import truss
from itertools import product

TEST_TRUSS_FILENAME = os.path.join(os.path.dirname(__file__), 'example.trs')


class TestSequenceFunctions(unittest.TestCase):

    def test_iterate_coordinates(self):

        c1 = list(product([2,3,4], range(2,5)))
        c2 = list(product(range(5,8), range(5,8)))
        c3 = list(product(range(8,12), range(2,5)))

        for j1 in c1:
            for j2 in c2:
                for j3 in c3:
                    print j1, j2, j3


    def test_build_methods(self):
        # Build truss from scratch
        t1 = truss.Truss()

        left_end = t1.add_joint(numpy.array([0.0, 0.0, 0.0]), d=2)
        left_end.roller(d=2)
        t1.add_joint(numpy.array([18.0/100.0, 0.0, 0.0]), d=2)
        right_end = t1.add_joint(numpy.array([36.0/100.0, 0.0, 0.0]), d=2)
        right_end.pinned()

        t1.add_joint(numpy.array([8.0/100.0, 6.0/100.0, 0.0]), d=2)
        t1.add_joint(numpy.array([18.0/100.0, 9.0/100.0, 0.0]), d=2)
        t1.add_joint(numpy.array([28.0/100.0, 6.0/100.0, 0.0]), d=2)


        t1.joints[1].loads[1] = -434
        
        t1.add_member(0, 1)
        t1.add_member(1, 2)

        t1.add_member(0, 3)
        t1.add_member(3, 4)
        t1.add_member(4, 5)
        t1.add_member(5, 2)

        t1.add_member(3, 1)
        t1.add_member(4, 1)
        t1.add_member(5, 1)

        t1.save_report(os.path.join(os.path.dirname(__file__), 'report_1.txt'))

    # def test_iterate_truss_experiments(self):

    #     c1 = list(product(range(5,15,2), range(5,15,2)))
    #     c2 = list(product(range(14,24,2), range(8,18,2)))
    #     c3 = list(product(range(20,30,2), range(8,18,2)))

    #     count = 0
    #     suspect = 0

    #     for j1 in c1:
    #         for j2 in c2:
    #             for j3 in c3:
    #                 count += 1
    #                 t = truss_analysis(j1,j2,j3)

    #     print count, suspect


def truss_analysis(j1, j2, j3):

    if j1[0]>=j2[0]:
        return
    if j2[0]>=j3[0]:
        return

#    print j1, j2, j3

    truss_being_tested = truss.Truss()

    left_end = truss_being_tested.add_joint(numpy.array([0.0, 0.0, 0.0]), d=2)
    left_end.roller(d=2)
    truss_being_tested.add_joint(numpy.array([18.0/100.0, 2.5/100.0, 0.0]), d=2)
    right_end = truss_being_tested.add_joint(numpy.array([36.0/100.0, 5.0/100.0, 0.0]), d=2)
    right_end.pinned()

    truss_being_tested.add_joint(numpy.array([j1[0]/100.0, j1[1]/100.0, 0.0]), d=2)
    truss_being_tested.add_joint(numpy.array([j2[0]/100.0, j2[1]/100.0, 0.0]), d=2)
    truss_being_tested.add_joint(numpy.array([j3[0]/100.0, j3[1]/100.0, 0.0]), d=2)

    truss_being_tested.joints[1].loads[1] = -2
    
    truss_being_tested.add_member(0, 1)
    truss_being_tested.add_member(1, 2)

    truss_being_tested.add_member(0, 3)
    truss_being_tested.add_member(3, 4)
    truss_being_tested.add_member(4, 5)
    truss_being_tested.add_member(5, 2)

    truss_being_tested.add_member(3, 1)
    truss_being_tested.add_member(4, 1)
    truss_being_tested.add_member(5, 1)

    truss_being_tested.calc_fos()


    return truss

if __name__ == "__main__":
    unittest.main()
