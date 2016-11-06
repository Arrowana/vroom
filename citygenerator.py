from matplotlib import pyplot as plt
import random
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point class ({}, {})'.format(self.x, self.y)

class Vertex:
    def __init__(self, point):
        self.point = point 
        self.neighboors = []

def vector(point_a, point_b):
    """Vector AB"""
    return point_b[0] - point_a[0], point_b[1] - point_a[1]

def vector_normal(point_a, point_b):
    vec = vector(point_a, point_b)
    norm = math.sqrt(vec[0]**2+vec[1]**2)

    return vec[0]/norm, vec[1]/norm

def get_random_vector(vector, l_min, l_max):
    f = random.uniform(l_min, l_max)
    return f*vector[0], f*vector[1]

def norm(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def candidate_validation(candidate, segments):
    """Check if the candidate is valid"""
    distance_min = 0.5 

    for pt1, pt2 in segments:
        if norm(candidate, pt1) < distance_min:
            candidate = pt1
            break
        if norm(candidate, pt2) < distance_min:
            candidate = pt2
            break

    print 'val'
    return candidate

def grid_growth(previous_point, current_point):
    p_forward = 0.8 #Probability of adding a point forward
    p_turn = 0.6 # Probability of adding a turn

    l_min = 5
    l_max = 10

    previous_vector = vector_normal(previous_point, current_point)

    n = -previous_vector[1], previous_vector[0] #Normal to previous segment
    candidates = []

    if random.random() <= p_forward:
        #Go straight 
        v = get_random_vector(previous_vector, l_min, l_max)
        new_point = current_point[0] + v[0], current_point[1] + v[1]
        candidates.append(new_point)

    if random.random() <= p_turn:
        n_scaled = get_random_vector(n, l_min, l_max)
        new_point = current_point[0] + n_scaled[0], current_point[1]+n_scaled[1]
        candidates.append(new_point)

    if random.random() <= p_turn:
        n_scaled = get_random_vector(n, l_min, l_max)
        new_point = current_point[0] - n_scaled[0], current_point[1]-n_scaled[1]
        candidates.append(new_point)

    return candidates

def generate():
    seed = [[0,0], [10,0]]
    segments = []
    queue = [seed] # queue of segments

    for i in range(500):
        previous_segment = queue[-1]
        candidates = grid_growth(*previous_segment)
        print(candidates)

        for candidate in candidates:
            #No check for now
            candidate = candidate_validation(candidate, segments)

            new_segment = [previous_segment[-1], candidate]
            print(new_segment)
            queue.append(new_segment)
            segments.append(new_segment)

    print(segments)
    for segment in segments:
        plt.plot(*zip(*segment))

    plt.show()
        

if __name__ == '__main__':
    generate()
