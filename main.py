import pygame
from math import cos, sin, radians

class Player(pygame.sprite.Sprite):
    OFFSET = 90 #Offset to get the car facing the right direction

    def __init__(self):
	self.start_pose_x = 50
	self.start_pose_y = 50

        surface = pygame.image.load('Audi.png')
        self.base_image = pygame.transform.scale(surface, (64, 64))
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect() # for drawing purpose
	
	self.pose = self.rect.copy() # actual pose of the vehicle
	self.pose.x = self.start_pose_x
	self.pose.y = self.start_pose_y

	self.L = 2

        self.speed = 0
        self.heading = 0
        self.steer = 0

	self.dt = 60

    def normalize(self, angle):
	return (angle+180)%360-180

    def update(self):
        heading_rad = radians(self.heading)
	steer_rad = radians(self.steer)

	dx = self.speed*cos(steer_rad)*cos(heading_rad)*self.dt
	dy = self.speed*cos(steer_rad)*sin(heading_rad)*self.dt
	dheading = self.speed*sin(steer_rad)/self.L*self.dt

        self.pose = self.pose.move(dx,-dy)
        self.heading = self.normalize(self.heading+dheading)


        self.image, self.rect = rot_center(self.base_image, 
            self.heading-self.OFFSET)

        print(self.rect)

        rect_x, rect_y = self.rect.topleft
        self.rect.left = self.pose.x + rect_x
        self.rect.top = self.pose.y + rect_y

        print "after", self.rect

	print "x: ",self.pose.x
	print "y: ",self.pose.y
	print "heading: ", self.heading

def rot_center(image, angle):
    """rotate a Surface, maintaining position."""
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite_rect = rot_sprite.get_rect(center=image.get_rect().center)

    return rot_sprite, rot_sprite_rect

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0

        self.width = width 
        self.height = height

    def update(self, target, track):
	# Limits the camera to the track perimeter
	if((target.pose.x-self.width/2)<track.rect.left):
            self.x = track.rect.left
	elif((target.pose.x+self.width/2)>track.rect.right):
	    self.x = self.width-track.rect.right
	else:
	    self.x = -target.pose.x + self.width/2

	if((target.pose.y-self.height/2)<track.rect.top):
            self.y = track.rect.top
	elif((target.pose.y+self.height/2)>track.rect.bottom):
	    self.y = self.height-track.rect.bottom
	else:
            self.y = -target.pose.y + self.height/2

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

    LEFT_PRESSED = False
    RIGHT_PRESSED = False

    camera = Camera(WIDTH, HEIGHT)
    track = Map()

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.speed += 0.1 
                if event.key == pygame.K_DOWN:
                    player.speed -= 0.1 
                elif event.key == pygame.K_LEFT:
		    LEFT_PRESSED = True
                    player.steer = 45 if (not RIGHT_PRESSED) else -45
                elif event.key == pygame.K_RIGHT:
		    RIGHT_PRESSED = True
                    player.steer = -45 if (not LEFT_PRESSED) else 45
            elif event.type == pygame.KEYUP:
		if event.key in [pygame.K_LEFT,pygame.K_RIGHT]:
		    if LEFT_PRESSED and RIGHT_PRESSED:
			player.steer = -player.steer
		    else:
			player.steer = 0
		    if event.key == pygame.K_LEFT:
                        LEFT_PRESSED = False
		    elif event.key == pygame.K_RIGHT:
		        RIGHT_PRESSED = False

        player.update()
        camera.update(player,track)

        screen.fill((0,0,0))

        for entity in [track, player]:
            screen.blit(entity.image, camera.apply(entity))

        pygame.display.flip()
        clock.tick(player.dt)
    
if __name__ == '__main__':
    play()
