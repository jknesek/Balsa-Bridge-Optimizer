import itertools
import numpy
import sys
import logging
from trussme import truss

def find_the_best_bridge():
    print "Analyizing Bridges..."
    logger = configure_logging()
    tuple_of_bridges = get_tuples()
    best_efficiency = 0.0
    best_bridge = None
    best_bridge_points = None
    best_supported_load = 0.0

    count = 0

    for bridge in tuple_of_bridges:
        if is_valid_truss(bridge):
            _truss, supported_load, efficiency = truss_efficiency(bridge, logger)
            logger.debug('Result for: ' + str(bridge) + ' load=' + str(supported_load) + ' mass=' + str(_truss.mass) + ' efficiency=' + str(efficiency))
            count += 1
            if count % 10000 == 0:
                print count
            if efficiency > best_efficiency:
                best_efficiency = efficiency
                best_bridge = _truss
                best_bridge_points = bridge
                best_supported_load = supported_load
                logger.debug('Best so far: ' + ' load=' + str(best_supported_load) + ' efficiency=' + str(best_efficiency))

    logger.info('Best: ' + str(best_bridge_points) + ' load=' + str(best_supported_load) + ' mass=' + str(best_bridge.mass) + ' efficiency=' + str(best_efficiency))
    best_bridge.save_report("best_5pt_bridge.txt")

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

    joint4 = truss_points_a[3]
    joint4_x = joint4[0]

    if joint3_x >= joint4_x:
        return False

    joint5 = truss_points_a[4]
    joint5_x = joint5[0]

    if joint4_x >= joint5_x:
        return False

    return True

def truss_efficiency(truss_points, logger):
    joint1 = truss_points[0]
    joint2 = truss_points[1]
    joint3 = truss_points[2]
    joint4 = truss_points[3]
    joint5 = truss_points[4]
    load_joint = truss_points[5]
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
    t1.add_joint(numpy.array([joint4[0]/100.0, joint4[1]/100.0, 0.0]), d=2)
    t1.add_joint(numpy.array([joint5[0]/100.0, joint5[1]/100.0, 0.0]), d=2)


    t1.joints[1].loads[1] = -100
    t1.load = -100
    
    t1.add_member(0, 1)
    t1.add_member(1, 2)

    t1.add_member(0, 3)
    t1.add_member(3, 4)
    t1.add_member(4, 5)
    t1.add_member(5, 6)
    t1.add_member(6, 7)
    t1.add_member(7, 2)

    t1.add_member(3, 1)
    t1.add_member(4, 1)
    t1.add_member(5, 1)
    t1.add_member(6, 1)
    t1.add_member(7, 1)

    t1.calc_mass()
    try:
        t1.calc_fos()
    except LinAlgError:
        logger.warn('Bridge geometry causes singular matrix, disqualifying: ' + str(truss_points))
        return t1, 0.0, 0.0

    if t1.result_suspect == True:
        logger.warn('Results possibly inacurate, disqualifying: ' + str(truss_points))
        return t1, 0.0, 0.0

    supported_load, efficiency = get_truss_load_and_efficiency(t1, logger)
    return t1, supported_load, efficiency


def configure_logging():
    # create logger with 'spam_application'
    logger = logging.getLogger('bridges')
    logger.setLevel(logging.INFO)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('bridges.log')
    fh.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    fh.setLevel(logging.INFO )
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def get_truss_load_and_efficiency(the_truss, logger):
    weakest_load = 1000000.0
    abs_load = abs(the_truss.load)
    for m in the_truss.members:
        logger.debug('force=' + str(m.force) + ' m.fos_yielding=' + str(m.fos_yielding) + ' m.fos_buckling=' + str(m.fos_buckling) + ' load=' + str(abs_load))
        if m.force > 0.0:
            supported_load = abs_load * m.fos_yielding / m.force
        else:
            if abs(m.fos_yielding) <= abs(m.fos_buckling):
                supported_load = abs_load * m.fos_yielding / m.force
            else:
                supported_load = abs_load * m.fos_buckling / m.force
        if supported_load < weakest_load:
            weakest_load = supported_load
    return weakest_load, weakest_load/the_truss.mass

def get_tuples():
    print "Getting All Tuples..."
    x1 = numpy.arange (2.0, 7.0, 1.0)
    y1 = numpy.arange (6.0, 12.0, 1.0)
    p1 = itertools.product (x1,y1)
    l1 = list(p1)

    x2 = numpy.arange (4.0, 13.0, 1.0)
    y2 = numpy.arange (14.0, 17.0, 1.0)
    p2 = itertools.product (x2,y2)
    l2 = list(p2)

    x3 = numpy.arange (14.0, 20.0, 1.0)
    y3 = numpy.arange (16.0, 21.0, 1.0)
    p3 = itertools.product (x3,y3)
    l3 = list(p3)

    x4 = numpy.arange (22.0, 29.0, 1.0)
    y4 = numpy.arange (14.0, 20.0, 1.0)
    p4 = itertools.product (x4,y4)
    l4 = list(p4)

    x5 = numpy.arange (28.0, 33.0, 1.0)
    y5 = numpy.arange (10.0, 15.0, 1.0)
    p5 = itertools.product (x5,y5)
    l5 = list(p5)

    load_points_list = []

    # all_x = numpy.arange (6.0, 10.0, 0.5)
    all_x = [18.5]
    for x in all_x:
        y = 5.0/36.0 * x
        p = (x, y)
        load_points_list.append(p)

    p6 = itertools.product (l1, l2, l3, l4, l5, load_points_list)
    # l4 = list(p4)  
    print len(x1) * len(x2) * len(x3) * len(x4) * len(x5) * len(all_x) * len(y1) * len(y2) * len(y3) * len(y4) * len(y5)
    return p6

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