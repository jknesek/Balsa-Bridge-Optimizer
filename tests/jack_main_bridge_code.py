import itertools
import numpy
import sys
import logging
from trussme import truss

def find_the_best_bridge():
    print "Analyizing Bridges..."
    logger = configure_logging()
    tuple_of_bridges = get_tuples()
    best_efficiency_so_far = 0.0
    best_bridge_so_far = None

    count = 0

    for bridge in tuple_of_bridges:
        if is_valid_truss(bridge):
            _truss, efficiency = truss_efficiency(bridge, logger)
            count += 1
            if count % 10000 == 0:
                print count
            if efficiency > best_efficiency_so_far:
                best_efficiency_so_far = efficiency
                best_bridge_so_far = _truss


    print best_efficiency_so_far
    best_bridge_so_far.print_and_save_report("best_bridge.txt")

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

def truss_efficiency(truss_points, logger):
    joint1 = truss_points[0]
    joint2 = truss_points[1]
    joint3 = truss_points[2]
    load_joint = truss_points[3]
    # Build truss from scratch
    t1 = truss.Truss()

    left_end = t1.add_joint(numpy.array([0.0, 0.0, 0.0]), d=2)
    left_end.roller(d=2)
    t1.add_joint(numpy.array([load_joint[0]/100.0, load_joint[1]/100, 0.0]), d=2)
    right_end = t1.add_joint(numpy.array([37.0/100.0, 5.14/100.0, 0.0]), d=2)
    right_end.pinned()

    t1.add_joint(numpy.array([joint1[0]/100.0, joint1[1]/100.0, 0.0]), d=2)
    t1.add_joint(numpy.array([joint2[0]/100.0, joint2[1]/100.0, 0.0]), d=2)
    t1.add_joint(numpy.array([joint3[0]/100.0, joint3[1]/100.0, 0.0]), d=2)


    t1.joints[1].loads[1] = -100
    t1.load = -100
    
    t1.add_member(0, 1)
    t1.add_member(1, 2)

    t1.add_member(0, 3)
    t1.add_member(3, 4)
    t1.add_member(4, 5)
    t1.add_member(5, 2)

    t1.add_member(3, 1)
    t1.add_member(4, 1)
    t1.add_member(5, 1)

    t1.calc_mass()
    try:
        t1.calc_fos()
    except LinAlgError:
        logger.warn('Probably weird bridge: ' + str(truss_points))
        return t1, 0.0

    efficiency = get_truss_efficiency(t1)
    return t1, efficiency


def configure_logging():
    # create logger with 'spam_application'
    logger = logging.getLogger('bridges')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('bridges.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def get_truss_efficiency(the_truss):
    weakest_load = 1000000.0
    abs_load = abs(the_truss.load)
    for m in the_truss.members:
        if m.force > 0:
            supported_load = abs_load * m.fos_yielding / m.force
        else:
            if m.fos_yielding > m.fos_buckling:
                supported_load = abs_load * m.fos_yielding / m.force
            else:
                supported_load = abs_load * m.fos_buckling / m.force
        if supported_load < weakest_load:
            weakest_load = supported_load
    return weakest_load/the_truss.mass

def get_tuples():
    print "Getting All Tuples..."
    x1 = range (4, 15)
    y1 = range (4, 14)
    p1 = itertools.product (x1,y1)
    l1 = list(p1)

    x2 = range (12, 23)
    y2 = range (9, 19)
    p2 = itertools.product (x2,y2)
    l2 = list(p2)

    x3 = range (20, 32)
    y3 = range (7, 16)
    p3 = itertools.product (x3,y3)
    l3 = list(p3)

    load_points_list = []

    all_x = range (11, 27)
    for x in all_x:
        y = 5.0/36.0 * x
        p = (x, y)
        load_points_list.append(p)

    p4 = itertools.product (l1, l2, l3, load_points_list)
    # l4 = list(p4)  
    # print l4
    return p4

# def get_tuples():
#     print "Getting All Tuples..."
#     x1 = range (3, 8)
#     y1 = range (4, 7)
#     p1 = itertools.product (x1,y1)
#     l1 = list(p1)

#     x2 = range (12, 16)
#     y2 = range (7, 12)
#     p2 = itertools.product (x2,y2)
#     l2 = list(p2)

#     x3 = range (19, 24)
#     y3 = range (7, 12)
#     p3 = itertools.product (x3,y3)
#     l3 = list(p3)

#     load_points_list = []

#     all_x = range (12, 28)
#     for x in all_x:
#         y = 5.0/36.0 * x
#         p = (x, y)
#         load_points_list.append(p)

#     p4 = itertools.product (l1, l2, l3, load_points_list)
#     # l4 = list(p4)  
#     # print l4
#     return p4


if __name__ == "__main__":
    find_the_best_bridge()