from matplotlib import pyplot as plt
import random
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Point class ({}, {})'.format(self.x, self.y)

class Vertex():
    def __init__(self, point, neighbours = None):
        self.point = point 
        
        if neighbours:
            self.neighbours = neighbours
        else:
            self.neighbours = []

    def __str__(self):
        return 'Vertex ({}, {})'.format(self.point[0], self.point[1])

    def __repr__(self):
        return '<Vertex point:({}, {})>'.format(self.point[0], self.point[1])

    def get_previous_vertex(self):
        return self.neighbours[-1]

def vector(point_a, point_b):
    """Vector AB"""
    return point_b[0] - point_a[0], point_b[1] - point_a[1]

def vector_normalized(point_a, point_b):
    vec = vector(point_a, point_b)
    norm = math.sqrt(vec[0]**2+vec[1]**2)

    return vec[0]/norm, vec[1]/norm

def get_random_vector(vector, l_min, l_max):
    f = random.uniform(l_min, l_max)
    return f*vector[0], f*vector[1]

def norm(a, b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def vector_minus(a, b):
    return a[0]-b[0], a[1]-b[1]

def line_param(a, b, t):
    return a[0] + t*b[0], a[1] + t*b[1]

def intersection(p, r, q, s):
    # p + t*q first line
    # r + u*s second line
    #source http://stackoverflow.com/a/565282

    u_num = dot(vector_minus(q, p), r)
    u_den = dot(r, s)

    if abs(u_den) < 0.001 and abs(u_num) < 0.001:
        # Colinear
        return None
    elif abs(u_den) < 0.001 and abs(u_num) >= 0.001:
        # Parallel
        return None

    t_num = dot(vector_minus(q, p), s)
    t = t_num/u_den
    u = u_num/u_den, u_num/u_den

    if abs(dot(r, s)) >= 0.001 and 0 < t and t < 1 and 0 < u and u < 1:
        #Two segment intersects
        return line_param(p, q, t)
    else:
        return None


def candidate_validation(candidate, previous_vertex, vertices):
    """Check if the candidate is valid, return a candidate vertex or None"""
    distance_min = 3 


    #Check if the vertex is intersecting any segment
    # Implemented if it crosses one line only
    for vertex in vertices:
        for neighbour in vertex.neighbours:
            inter = intersection(previous_vertex.point, candidate, vertex.point, neighbour.point)
            if inter:
                print 'Inter'
                candidate = inter

                vertex_candidate = Vertex(candidate, neighbours=[vertex, neighbour])

                vertex.neighbours.remove(neightbour)
                vertex.neighbours.append(vertex_candidate)

                neightbour.neightbours.remove(vertex)
                neightbour.neighbours.append(vertex_candidate)

                return vertex_candidate

    # check for points nearby and replace the candidate with it
    for vertex in vertices:
        if norm(candidate, vertex.point) < distance_min:
            vertex_candidate = vertex
            print 'link to existing intersection'
            return vertex_candidate

    print 'val'
    vertex_candidate = Vertex(candidate)
    return vertex_candidate

def grid_growth(vertex):
    p_forward = 0.8 #Probability of adding a point forward
    p_turn = 0.6 # Probability of adding a turn

    l_min = 5
    l_max = 10

    previous_point = vertex.point
    previous_vector = vector_normalized(vertex.get_previous_vertex().point, vertex.point)

    n = -previous_vector[1], previous_vector[0] #Normal to previous segment
    candidates = []

    if random.random() <= p_forward:
        #Go straight 
        v = get_random_vector(previous_vector, l_min, l_max)
        new_point = previous_point[0] + v[0], previous_point[1] + v[1]
        candidates.append(new_point)

    if random.random() <= p_turn:
        n_scaled = get_random_vector(n, l_min, l_max)
        new_point = previous_point[0] + n_scaled[0], previous_point[1]+n_scaled[1]
        candidates.append(new_point)

    if random.random() <= p_turn:
        n_scaled = get_random_vector(n, l_min, l_max)
        new_point = previous_point[0] - n_scaled[0], previous_point[1]-n_scaled[1]
        candidates.append(new_point)

    return candidates

def test_grid_growth():
    pass

def generate():
    start = Vertex([0,0])
    second_point = Vertex([10, 0], neighbours=[start])
    start.neighbours = [second_point]

    vertices = [start, second_point] #All generated and valid vertices
    queue = [second_point] # queue of vertices

    for i in range(500):
        previous_vertex = queue[-1]
        print 'previous_vertex:', previous_vertex
        candidates = grid_growth(previous_vertex)
        print 'candidates:', candidates

        for candidate in candidates:
            vertex_candidate = candidate_validation(candidate, previous_vertex, vertices)

            if vertex_candidate in vertices:
                print 'Already in'
                vertex_candidate.neighbours.append(previous_vertex)
            else:
                vertex_candidate.neighbours.append(previous_vertex)
                queue.append(vertex_candidate)
                vertices.append(vertex_candidate)

    print vertices[:10]

    for vertex in vertices:
        for neighbour in vertex.neighbours:
            plt.plot(*zip(*[vertex.point, neighbour.point]))

    plt.show()
        

if __name__ == '__main__':
    generate()
