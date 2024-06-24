#!/usr/bin/env/python3
# Game v3

import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-bit SpaceX Starship Lander Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Starship properties
starship_width, starship_height = 40, 80
starship_x = WIDTH // 2 - starship_width // 2
starship_y = HEIGHT // 2
starship_speed_y = 0
starship_speed_x = 0
gravity = 0.05

# Game state
altitude = 10000  # 10km
speed = 0
fuel = 100

font = pygame.font.Font(None, 36)

def draw_starship(screen, x, y, thrusting):
    pygame.draw.rect(screen, WHITE, (x, y, starship_width, starship_height))
    if thrusting:
        pygame.draw.polygon(screen, RED, [
            (x + starship_width // 2, y + starship_height),
            (x + starship_width // 2 - 10, y + starship_height + 20),
            (x + starship_width // 2 + 10, y + starship_height + 20)
        ])

def create_gradient_background(width, height):
    background = pygame.Surface((width, height))
    for y in range(height):
        color = [min(255, int(128 * y / height)), 0, 0]  # Red gradient
        pygame.draw.line(background, color, (0, y), (width, y))
    return background

background = create_gradient_background(WIDTH, HEIGHT)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    thrusting = keys[pygame.K_SPACE] and fuel > 0

    if keys[pygame.K_LEFT]:
        starship_speed_x = -2
    elif keys[pygame.K_RIGHT]:
        starship_speed_x = 2
    else:
        starship_speed_x = 0

    if thrusting:
        starship_speed_y -= 0.1
        fuel -= 0.1

    starship_speed_y += gravity
    altitude -= starship_speed_y
    starship_x += starship_speed_x
    speed = abs(starship_speed_y)

    # Keep starship on screen
    starship_x = max(0, min(starship_x, WIDTH - starship_width))

    # Drawing
    screen.blit(background, (0, 0))
    draw_starship(screen, starship_x, starship_y, thrusting)

    # HUD
    hud_text = f"Altitude: {int(altitude)}  Speed: {speed:.1f}  Fuel: {int(fuel)}"
    hud_render = font.render(hud_text, True, WHITE)
    screen.blit(hud_render, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()