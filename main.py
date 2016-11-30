import pygame
from player import Player
from camera import Camera
import client

class Map(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('track.png')
		self.rect = self.image.get_rect()

	def draw(self, screen):
		screen.blit(self.image, self.rect)

def handle_event(event, player, key_state):
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_UP:
			player.speed += 0.1
		if event.key == pygame.K_DOWN:
			player.speed -= 0.1
		elif event.key == pygame.K_LEFT:
			key_state.left_pressed = True
			player.steer = 45 if not key_state.right_pressed else -45
		elif event.key == pygame.K_RIGHT:
			key_state.left_pressed = True
			player.steer = -45 if not key_state.right_pressed else 45
	elif event.type == pygame.KEYUP:
		if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
			if key_state.left_pressed and key_state.right_pressed:
				player.steer = -player.steer
			else:
				player.steer = 0
			if event.key == pygame.K_LEFT:
				key_state.left_pressed = False
			elif event.key == pygame.K_RIGHT:
				key_state.right_pressed = False

class KeyState:
	def __init__(self):
		self.left_pressed = False
		self.right_pressed = False

def play():
	pygame.init()

	WIDTH, HEIGHT = 800, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Thecargame')

	clock = pygame.time.Clock()

	player = Player()

	network_entities = []
	network_handler = client.NetworkHandler('127.0.0.1', 5755, network_entities)

	key_state = KeyState()

	camera = Camera(WIDTH, HEIGHT)
	track = Map()

	while True:
		for event in pygame.event.get():
			handle_event(event, player, key_state)

		player.update()
		print [e.userid for e in network_entities]
		camera.update(player, track)

		network_handler.update(player)

		screen.fill((0,0,0))

		for entity in [track, player] + network_entities:
			screen.blit(entity.image, camera.apply(entity))

		pygame.display.flip()
		clock.tick(player.dt)
	
if __name__ == '__main__':
	play()
