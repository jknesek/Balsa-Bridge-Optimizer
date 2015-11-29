import unittest
import itertools

class TestBasicPythonCode(unittest.TestCase):



    def test_loop_through_list(self):
        x1 = range (2, 6)
        y1 = range (2, 5)
        p1 = itertools.product (x1,y1)
        l1 = list(p1)
        #for a in x:
           #for b in y:
              #print a, b
        x2 = range (2, 6)
        y2 = range (2, 5)
        p2 = itertools.product (x2,y2)
        l2 = list(p2)

        x3 = range (2, 6)
        y3 = range (2, 5)
        p3 = itertools.product (x3,y3)
        l3 = list(p3)


        p4 = itertools.product (l1, l2, l3)
        l4 = list(p4)

        for a in l4:
            print a

    def test_load_line(self):
        all_x = range (0, 36)
        for x in all_x:
            y = 5.0/36.0 * x
            print (x, y)

    def test_slope_check(self):
        all_x = range (1,5)
        for x in all_x:
            slope = 4/x
            if slope > 2:
                print (x, 4)
                print "False"
            else:
                print (x, 4)
                print "True"

    def test_slope_is_too_high(self):
        truss_points = ((3,8), (10,6), (25,5), (27, 3.75))
        self.assertFalse(is_valid_truss(truss_points))

    def test_slope_is_at_limit(self):
        truss_points = ((1,2), (10,6), (25,5), (27, 3.75))
        self.assertTrue(is_valid_truss(truss_points))

    def test_slope_is_good(self):
        truss_points = ((1,1), (10,6), (25,5), (27, 3.75))
        self.assertTrue(is_valid_truss(truss_points))

    def test_j1_and_j2_x_is_same(self):
        truss_points = ((3,2), (3,6), (25,5), (27, 3.75))
        self.assertFalse(is_valid_truss(truss_points))

    def test_j1_x_is_less(self):
        truss_points = ((2,2), (3,6), (25,5), (27, 3.75))
        self.assertTrue(is_valid_truss(truss_points))

    def test_j1_x_is_more(self):
        truss_points = ((4,2), (3,6), (25,5), (27, 3.75))
        self.assertFalse(is_valid_truss(truss_points))

    def test_j2_and_j3_x_is_same(self):
        truss_points = ((1,2), (10,6), (10,5), (27, 3.75))
        self.assertFalse(is_valid_truss(truss_points))

    def test_j2_x_is_less(self):
        truss_points = ((2,2), (10,6), (11,5), (27, 3.75))
        self.assertTrue(is_valid_truss(truss_points))

    def test_j2_x_is_more(self):
        truss_points = ((4,2), (10,6), (9,5), (27, 3.75))
        self.assertFalse(is_valid_truss(truss_points))

def is_valid_truss(truss_points_a):
    joint1 = truss_points_a[0]
    joint1_x = joint1[0]
    joint1_y = joint1[1]
    
    if joint1_y/joint1_x > 2.0:
        return False

    joint2 = truss_points_a[1]
    joint2_x = joint2[0]

    if joint1_x >= joint2_x:
        return False

    joint3 = truss_points_a[2]
    joint3_x = joint3[0]

    if joint2_x >= joint3_x:
        return False

    return True



def truss_analysis(j1, j2, j3):
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

    truss_being_tested.calc_fos()

    return truss




if __name__ == "__main__":
    unittest.main()

