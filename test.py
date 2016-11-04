import pygame
import math

def generate_parallel(curve, distance):
    parallel = []
    for pt1, pt2 in zip(curve[:-1], curve[1:]):
        n = (-(pt2[1]-pt1[1]), pt2[0] - pt1[0])
        norm = math.sqrt(n[0]**2+n[1]**2)
        n = (n[0]/norm, n[1]/norm)

        new_point = (pt1[0] + distance*n[0], pt1[1] + distance*n[1])
        parallel.append(new_point)

    return parallel

def play():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Thecargame')

    clock = pygame.time.Clock()
    points = [[100, 100], [300, 100], [400, 600]]

    def curve(x):
        u = (20*x/500.)
        return 200*math.sin(x/(2*math.pi)/25) + 300

    white = (255, 255, 255)
    asphalt = (40, 43, 42)

    road_width = 50
    saved = False

    while True:
        screen.fill((0,0,0))

        surface = pygame.surface.Surface((800, 600))
        pygame.draw.rect(screen, (0,0,255), (100,100, 200, 300))
        pygame.draw.line(screen, (255,0,0), (0,0), (100,100))
        for pt1, pt2 in zip(points[:-1], points[1:]):
            pygame.draw.line(screen, (0, 255, 0), pt1, pt2)


        road_middle = [(x, curve(x)) for x in range(1000)]

        road_left = generate_parallel(road_middle, road_width)
        road_right = generate_parallel(road_middle, -road_width)

        #pygame.draw.lines(screen, asphalt, False, road_middle, 2*road_width)

        pygame.draw.polygon(surface, asphalt, road_left+road_right[::-1])#+road_middle[::-1])

        #Draw dashed line on the middle of the road
        segments_to_keep = [segment for i, segment in enumerate(zip(road_middle[:-1], road_middle[1:])) if i % 6 == 0]
        print len(road_middle), len(segments_to_keep)
        for pt1, pt2 in segments_to_keep:
            pygame.draw.line(surface, white, pt1, pt2, 2)

        pygame.draw.lines(surface, white, False, road_left, 2)
        pygame.draw.lines(surface, white, False, road_right, 2)

        screen.blit(surface, surface.get_rect())

        if not saved:
            pygame.image.save(surface, 'test.png')
            saved = True

        pygame.display.flip()

        clock.tick(60)
play()
