import pygame

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

