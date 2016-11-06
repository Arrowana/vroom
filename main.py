import pygame
import math

class Player(pygame.sprite.Sprite):
    OFFSET = 90 #Offset to get the car facing the right direction

    def __init__(self):
        surface = pygame.image.load('Audi.png')
        self.base_image = pygame.transform.scale(surface, (64, 64))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()

        self.speed = 0
        self.heading = 0
        self.steer = 0

        self.x = 0
        self.y = 0

    def update(self):
        heading_radians = math.radians(self.heading)
        self.x += self.speed*math.cos(heading_radians) 
        self.y += -self.speed*math.sin(heading_radians)

        self.heading += 2*self.steer
        self.image, self.rect = rot_center(self.base_image, self.heading-self.OFFSET)

        self.rect.left = self.x
        self.rect.top = self.y

def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite_rect = rot_sprite.get_rect(center=image.get_rect().center)  #rot_image is not defined 

    return rot_sprite, rot_sprite_rect

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0

        self.width = width 
        self.height = height

    def update(self, target):
        self.x = -target.x + self.width/2
        self.y = -target.y + self.height/2

    def apply(self, target):
        return target.rect.move(self.x, self.y)

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('track.png')
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def play():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Thecargame')

    clock = pygame.time.Clock()

    player = Player()

    camera = Camera(WIDTH, HEIGHT)
    track = Map()

    while True:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speed += 3 
                if event.key == pygame.K_DOWN:
                    player.speed -= 3 
                elif event.key == pygame.K_LEFT:
                    player.steer = 1
                elif event.key == pygame.K_RIGHT:
                    player.steer = -1
            elif event.type == pygame.KEYUP:
                player.steer = 0

        player.update()
        camera.update(player)

        screen.fill((0,0,0))

        for entity in [track, player]:
            screen.blit(entity.image, camera.apply(entity))

        #player.draw(screen)

        pygame.draw.line(screen, (255,0,0), (0,0), (100,100))
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == '__main__':
    play()
