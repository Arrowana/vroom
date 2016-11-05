import pygame
from math import cos,sin,radians

class Player():
    OFFSET = 90

    def __init__(self):
	self.start_pose_x = 50
	self.start_pose_y = 50

        self.car = pygame.transform.scale(pygame.image.load('Audi.png'), (64, 64))
        self.rect = self.car.get_rect() # for drawing purpose
	
	self.pose = self.rect.copy() # actual pose of the vehicle
	self.pose.x = self.start_pose_x
	self.pose.y = self.start_pose_y

	self.L = 2

        self.speed = 0
        self.heading = 0
        self.steer = 0

	self.dt = 60

    def normalize(self,angle):
	return (angle+180)%360-180

    def update(self):
        heading_rad = radians(self.heading)
	steer_rad = radians(self.steer)

	dx = self.speed*cos(steer_rad)*cos(heading_rad)*self.dt
	dy = self.speed*cos(steer_rad)*sin(heading_rad)*self.dt
	dheading = self.speed*sin(steer_rad)/self.L*self.dt

        self.pose = self.pose.move(dx,-dy)
        self.heading = self.normalize(self.heading+dheading)

	print "x: ",self.pose.x
	print "y: ",self.pose.y
	print "heading: ", self.heading

    def draw(self, screen):
        car_rotated = pygame.transform.rotate(self.car, self.heading-Player.OFFSET)

	self.rect.x = self.pose.x-car_rotated.get_rect().width/2
	self.rect.y = self.pose.y-car_rotated.get_rect().height/2
	
        screen.blit(car_rotated, self.rect)

def play():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Thecargame')

    clock = pygame.time.Clock()

    player = Player()

    LEFT_PRESSED = False
    RIGHT_PRESSED = False

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

        screen.fill((0,0,0))
        player.draw(screen)
        pygame.display.flip()
        clock.tick(player.dt)
    
if __name__ == '__main__':
    play()
