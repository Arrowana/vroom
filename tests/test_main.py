import pygame
import game_object
import game_event
import os

class SimEvent():
	def __init__(self, key=None, type=None):
		self.key = key
		self.type = type

def test_handle_event():
	player1 = game_object.Player()
	player2 = game_object.Player()
	player3 = game_object.Player()

	game_event.handle_event(SimEvent(pygame.K_UP, pygame.KEYDOWN), player1, game_event.KeyState())
	assert player1.speed == 0.1

	game_event.handle_event(SimEvent(pygame.K_DOWN, pygame.KEYDOWN), player2, game_event.KeyState())
	assert player2.speed == -0.1

	key_state3 = game_event.KeyState()
	game_event.handle_event(SimEvent(pygame.K_LEFT, pygame.KEYDOWN), player3, key_state3)
	assert key_state3.left_pressed == True and player3.steer == 45
	game_event.handle_event(SimEvent(pygame.K_LEFT, pygame.KEYUP), player3, key_state3)
	assert key_state3.left_pressed == False and player3.steer == 0

