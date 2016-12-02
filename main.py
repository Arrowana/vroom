import pygame
import game_object
from camera import Camera
import game_event
import client
import time
import sys

class Map(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('track.png')
		self.rect = self.image.get_rect()

	def draw(self, screen):
		screen.blit(self.image, self.rect)

def play(multiplayer_mode = False):
	pygame.init()

	WIDTH, HEIGHT = 800, 600
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Thecargame')

	clock = pygame.time.Clock()

	player = game_object.Player()

	network_entities = []
	if multiplayer_mode:
		network_handler = client.NetworkHandler('127.0.0.1', 5755, network_entities)

	key_state = game_event.KeyState()

	camera = Camera(WIDTH, HEIGHT)
	track = Map()

	while True:
		for event in pygame.event.get():
			game_event.handle_event(event, player, key_state)

		player.update()
		print [e.userid for e in network_entities]
		camera.update(player, track)

		now = time.time()
		if multiplayer_mode:
			network_handler.update(player)
		duration = time.time() - now
		print duration

		screen.fill((0,0,0))

		for entity in [track, player] + network_entities:
			screen.blit(entity.image, camera.apply(entity))

		pygame.display.flip()
		clock.tick(player.dt)
	
if __name__ == '__main__':
	if len(sys.argv) > 1:
		if sys.argv[1] == '-m':
			play(multiplayer_mode=True)	
		else:
			print 'Argument not recognised'
	else:
		play()
