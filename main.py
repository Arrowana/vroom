import pygame
import math

class Player():
    OFFSET = 90

    def __init__(self):
        self.car = pygame.transform.scale(pygame.image.load('Audi.png'), (64, 64))
        self.rect = self.car.get_rect()

        self.speed = 0
        self.heading = 0
        self.steer = 0

    def update(self):
        heading_radians = math.radians(self.heading)
        self.rect = self.rect.move(self.speed*math.cos(heading_radians), 
            -self.speed*math.sin(heading_radians))

        self.heading += 4*self.steer

    def draw(self, screen):
        car_rotated = pygame.transform.rotate(self.car, self.heading-Player.OFFSET)
        screen.blit(car_rotated, self.rect)

def play():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Thecargame')

    clock = pygame.time.Clock()

    player = Player()

    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speed += 5 
                if event.key == pygame.K_DOWN:
                    player.speed -= 5 
                elif event.key == pygame.K_LEFT:
                    player.steer = 1
                elif event.key == pygame.K_RIGHT:
                    player.steer = -1
            elif event.type == pygame.KEYUP:
                player.steer = 0

        player.update()

        screen.fill((0,0,0))
        player.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == '__main__':
    play()
