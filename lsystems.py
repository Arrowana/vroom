"""
    Test using L-systems rules listed on wikipedia
"""
import re
from matplotlib import pyplot as plt
import math

class Lsystem:
    def __init__(self, rules):
        self.rules = rules

    def run(self, start, iterations):
        result = start

        r = re.compile('|'.join(self.rules.keys()))

        for i in range(iterations):
            result = r.sub(lambda m: self.rules[m.group(0)], result)

        return result
                 
def test_algae():
    system = Lsystem({'A': 'AB', 'B': 'A'})

    assert system.run('A', 6) == 'ABAABABAABAABABAABABA'
    assert system.run('A', 7) == 'ABAABABAABAABABAABABAABAABABAABAAB'

def test_pythagoras_tree():
    system = Lsystem({'1': '11', '0': '1[0]0'})

    assert system.run('0', 3) == '1111[11[1[0]0]1[0]0]11[1[0]0]1[0]0'

def run_tests():
    test_algae()
    test_pythagoras_tree()

def test_tree():
    system=Lsystem({'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'})
    result=system.run('X', 2)
    print(result)

def turtle_graphics(pattern, angle_increment = 25):
    start = [0,0]
    segments = []

    stack = []
    pos = start
    angle = 0

    for char in pattern:
        if char == '0':
            new_pos = [pos[0] + math.cos(math.radians(angle)),
                pos[1] + math.sin(math.radians(angle))]

            segments.append([pos, new_pos])
            pos = new_pos
        elif char == '1':
            new_pos = [pos[0] + math.cos(math.radians(angle)),
                pos[1] + math.sin(math.radians(angle))]

            segments.append([pos, new_pos])
            pos = new_pos
        elif char == '[':
            stack.append([pos, angle])
            angle += angle_increment
        elif char == ']':
            pos, angle = stack.pop()
            angle -= angle_increment

    return segments

def turtle_graphics_tree(pattern, angle_increment = 27):
    start = [0,0]
    segments = []

    stack = []
    pos = start
    angle = 0

    for char in pattern:
        if char == 'F':
            new_pos = [pos[0] + math.cos(math.radians(angle)),
                pos[1] + math.sin(math.radians(angle))]

            segments.append([pos, new_pos])
            pos = new_pos
        elif char == '-':
            angle += angle_increment
        elif char == '+':
            angle -= angle_increment
        elif char == '[':
            stack.append([pos, angle])
        elif char == ']':
            pos, angle = stack.pop()

    print('{} segments generated'.format(len(segments)))
    return segments
    

def display(segments):
    for zipped_segment in [zip(*segment) for segment in segments]:
        plt.plot(*zipped_segment)
    plt.axis('equal')
    plt.show()

def draw_system(pattern):
    segments = turtle_graphics(pattern)
    display(segments)

#draw_system(Lsystem({'1': '11[01', '0': '1[0]0'}).run('0', 5))
#display(turtle_graphics_tree(Lsystem({'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}).run('X', 7)))
display(turtle_graphics_tree(Lsystem({'X': 'F[+X][-X]FX', 'F': 'FF'}).run('X', 7), angle_increment = 25.7))
