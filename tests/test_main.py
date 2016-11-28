import pygame
from player import Player
import main

class SimEvent():
	def __init__(self, key=None, type=None):
		self.key = key
		self.type = type

def test_handle_event():
	player1 = Player()
	player2 = Player()
	player3 = Player()

	main.handle_event(SimEvent(pygame.K_UP, pygame.KEYDOWN), player1, main.KeyState())
	assert player1.speed == 0.1

	main.handle_event(SimEvent(pygame.K_DOWN, pygame.KEYDOWN), player2, main.KeyState())
	assert player2.speed == -0.1

	key_state3 = main.KeyState()
	main.handle_event(SimEvent(pygame.K_LEFT, pygame.KEYDOWN), player3, key_state3)
	assert key_state3.left_pressed == True and player3.steer == 45
	main.handle_event(SimEvent(pygame.K_LEFT, pygame.KEYUP), player3, key_state3)
	assert key_state3.left_pressed == False and player3.steer == 0

