#!/usr/bin/env/python3

import pygame
import random

pygame.init()

WIDTH, HEIGHT = 640, 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-bit Starship Landing System")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ship properties
starship_width, starship_height = 40, 80
starship_x = WIDTH // 2 - starship_width // 2
starship_y = 0
starship_speed_y = 0
starship_speed_x = 0

gravity = 0.1

# landing pad properties
pad_width = 100
pad_height = 20
pad_x = random.randint(0, WIDTH - pad_width)
pad_y = HEIGHT - pad_height

# T
score = 0
game_over = False
font = pygame.font.Font(None, 36)

# Main game loop

running = True
clock = pygame.time.Clock()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				starship_speed_y = -2 # applies thrust to starship
			elif event.key == pygame.K_r and game_over:
				# game resets
				starship_x = WIDTH // 2 - starship_width // 2
				starship_y = 0
				starship_speed_y = 0
				starship_speed_x = 0
				pad_x = random.randint(0, WIDTH - pad_width)
				score = 0
				game_over = False

	if not game_over:
		# continuity in game
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			starship_speed_x = -2
		elif keys[pygame.K_RIGHT]:
			starship_speed_x = -2
		else:
			starship_speed_x = 0
		

		# updating the position of starship
		starship_speed_y += gravity
		starship_y += starship_speed_y
		starship_x += starship_speed_x

		# keep the ship on screen always
		starship_x = max(0, min(starship_x, WIDTH - starship_width))

		# check for landing/crash
		if (starship_y > HEIGHT - starship_height):
			if (pad_x < starship_x < pad_x + pad_width - starship_width and
			 starship_speed_y < 2):
				score += 100
				starship_y = HEIGHT - starship_height - pad_height
				starship_speed_y = 0
			else:
				game_over = True

		screen.fill(BLACK)

		# Drawing starship
		pygame.draw.rect(screen, WHITE, (starship_x, starship_y, starship_width, starship_height))

		# Drawing landing pad
		pygame.draw.rect(screen, GREEN, (pad_x, pad_y, pad_width, pad_height))

		# Drawing the score
		score_text = font.render(f"Score: {score}", True, WHITE)
		screen.blit(score_text, (10, 10))

		# Drawing the game over message
		if game_over:
			game_over_text = font.render("Game Over! Press R to restart", True, RED)
			screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))


		# Updating the display and cap the frame rate at 120
		pygame.display.flip()
		clock.tick(120)

pygame.quit()
