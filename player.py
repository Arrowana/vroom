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

		debug_pose(self.pose, self.heading)

def rot_center(image, angle):
	"""rotate a Surface, maintaining position."""
	rot_sprite = pygame.transform.rotate(image, angle)
	rot_sprite_rect = rot_sprite.get_rect(center=image.get_rect().center)

	return rot_sprite, rot_sprite_rect

def debug_pose(pose, heading):
	print "x: ", pose.x
	print "y: ", pose.y
	print "heading: ", heading

