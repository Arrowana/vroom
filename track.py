from matplotlib import pyplot as plt
from random import random
import math
import numpy

import pdb

def convex_hull(points_input):
    points = points_input[:]
    points = sorted(points, key=lambda x: x[0])
    print(points)

    U=[]
    L=[]

    def cross_product(o, a, b):
        return (a[0] - o[0])*(b[1] - o[1]) -\
            (a[1] - o[1])*(b[0] - o[0])

    for point in points:
        while len(L) > 1 and cross_product(L[-2], L[-1], point) <= 0:
            L.pop()
        L.append(point)

    for point in points[::-1]:
        while len(U) > 1 and cross_product(U[-2], U[-1], point) <= 0:
            U.pop()
        U.append(point)

    return L[:-1]+U[:-1]

def add_points(points):
    points_output = points[:]
    for point_a, point_b in zip(points[:-1], points[1:]):

        x = 10*random()
        y = 10*random()

        point_i = [(point_a[0]+point_b[0])/2+x, (point_a[1] + point_b[1])/2+y]
        points_output.extend([point_a, point_i, point_b])

    return points_output

def CatmullRomSpline(P0, P1, P2, P3, nPoints=100):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    alpha = 0.5
    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    # Only calculate points between P1 and P2
    t = numpy.linspace(t1,t2,nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t),1)

    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
    return C

def CatmullRomChain(P):
    """
    Calculate Catmull Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x,y) points.
    C = []
    for i in range(sz-3):
        c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
        C.extend(c)

    return C

def generate():
    width = 100
    height = 100

    scale = 150 

    points = [(scale*random(), scale*random()) for i in range(10)]

    hull=convex_hull(points)
    with_more = add_points(hull)

    C=CatmullRomChain(with_more)
    print C

    pdb.set_trace()
    print 'points:', points
    print 'hull:', hull

    plt.title('Final')
    plt.plot(*zip(*points))
    plt.plot(*zip(*hull))
    plt.plot(*zip(*with_more), marker='*')
    x,y = zip(*C)
    plt.plot(x,y)
    plt.axis('equal')

    plt.show()

if __name__ == '__main__':
    generate()
