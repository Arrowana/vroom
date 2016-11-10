import math

def generate_parallel(curve, distance):
    parallel = []
    for pt1, pt2 in zip(curve[:-1], curve[1:]):
        n = (-(pt2[1]-pt1[1]), pt2[0] - pt1[0])
        norm = math.sqrt(n[0]**2+n[1]**2)
        n = (n[0]/norm, n[1]/norm)

        new_point = [pt1[0] + distance*n[0], pt1[1] + distance*n[1]]
        parallel.append(new_point)

    return parallel

