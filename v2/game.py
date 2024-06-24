#!/usr/bin/env/python3
# Game v2

import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starship Landing Simulator")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load images (replace with your own image files)
starship_img = pygame.Surface((40, 120))  # Placeholder
starship_img.fill(WHITE)
moon_img = pygame.Surface((60, 60))  # Placeholder
moon_img.fill(WHITE)
star_img = pygame.Surface((2, 2))  # Placeholder
star_img.fill(WHITE)

# Starship properties
starship_width, starship_height = 40, 120
starship_x = WIDTH // 2 - starship_width // 2
starship_y = HEIGHT // 2
starship_speed_y = 0
starship_speed_x = 0
starship_angle = 0
gravity = 0.1

# Game state
altitude = 10000  # Start at 10km altitude
speed = 0
fuel_used = 0
max_fuel = 1000

# Landing pad
pad_width = 100
pad_height = 20
pad_x = random.randint(0, WIDTH - pad_width)

font = pygame.font.Font(None, 36)

class Particle:
    def __init__(self, x, y, color, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class ParticleSystem:
    def __init__(self, x, y, color, count, size_range, speed_range_x, speed_range_y):
        self.particles = []
        for _ in range(count):
            size = random.uniform(*size_range)
            speed_x = random.uniform(*speed_range_x)
            speed_y = random.uniform(*speed_range_y)
            self.particles.append(Particle(x, y, color, size, speed_x, speed_y))

    def update(self):
        for particle in self.particles:
            particle.move()

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

# Create particle systems
stars = ParticleSystem(0, 0, (255, 255, 255), 200, (1, 3), (-0.5, 0.5), (0.1, 0.5))
thrust_flames = ParticleSystem(0, 0, (255, 100, 0), 100, (3, 8), (-1, 1), (2, 5))

def draw_starship(screen, x, y, angle, thrusting):
    rotated_ship = pygame.transform.rotate(starship_img, angle)
    new_rect = rotated_ship.get_rect(center=starship_img.get_rect(topleft=(x, y)).center)
    screen.blit(rotated_ship, new_rect.topleft)
    if thrusting:
        thrust_flames.particles = [Particle(x + starship_width // 2, y + starship_height, (255, 100, 0), 
                                            random.uniform(3, 8), random.uniform(-1, 1), random.uniform(2, 5)) 
                                   for _ in range(100)]
        thrust_flames.update()
        thrust_flames.draw(screen)

def create_gradient_surface(width, height, start_color, end_color):
    surface = pygame.Surface((width, height))
    for y in range(height):
        r = start_color[0] + (end_color[0] - start_color[0]) * y / height
        g = start_color[1] + (end_color[1] - start_color[1]) * y / height
        b = start_color[2] + (end_color[2] - start_color[2]) * y / height
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
    return surface

atmospheric_gradient = create_gradient_surface(WIDTH, HEIGHT, (0, 0, 0), (255, 0, 0))

def draw_hud(screen, altitude, speed, fuel_used):
    altitude_text = font.render(f"Altitude: {int(altitude)}m", True, WHITE)
    speed_text = font.render(f"Speed: {int(speed)}m/s", True, WHITE)
    fuel_text = font.render(f"Fuel Used: {int(fuel_used)}L", True, WHITE)
    
    screen.blit(altitude_text, (10, 10))
    screen.blit(speed_text, (10, 50))
    screen.blit(fuel_text, (10, 90))

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    thrusting = keys[pygame.K_SPACE]
    
    if keys[pygame.K_a]:
        starship_speed_x = -2
        starship_angle = min(starship_angle + 1, 15)
    elif keys[pygame.K_d]:
        starship_speed_x = 2
        starship_angle = max(starship_angle - 1, -15)
    else:
        starship_speed_x = 0
        starship_angle = starship_angle * 0.95  # Gradually return to vertical

    if thrusting and fuel_used < max_fuel:
        starship_speed_y -= 0.2
        fuel_used += 1

    starship_speed_y += gravity
    altitude -= starship_speed_y
    starship_x += starship_speed_x
    
    # Keep starship relatively centered, but allow some movement
    starship_x = max(WIDTH * 0.25, min(starship_x, WIDTH * 0.75))
    
    speed = abs(starship_speed_y)

    # Drawing
    screen.fill((0, 0, 50))  # Dark blue space background
    
    # Draw stars
    stars.update()
    stars.draw(screen)
    
    # Draw moon
    screen.blit(moon_img, (WIDTH - 100, 50))
    
    # Draw atmospheric entry effect
    if altitude < 5000:
        alpha = int(255 * (1 - altitude / 5000))
        atmospheric_gradient.set_alpha(alpha)
        screen.blit(atmospheric_gradient, (0, 0))
    
    # Draw landing pad
    pad_y = HEIGHT - pad_height - (altitude if altitude < HEIGHT else HEIGHT)
    if pad_y > 0:
        pygame.draw.rect(screen, GREEN, (pad_x, pad_y, pad_width, pad_height))
    
    draw_starship(screen, starship_x, starship_y, starship_angle, thrusting)
    
    draw_hud(screen, altitude, speed, fuel_used)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()