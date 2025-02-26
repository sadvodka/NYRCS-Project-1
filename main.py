import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Circle and Avoid Obstacles (Maze)")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the player's attributes
player_radius = 20
player_x = width // 2
player_y = height // 2
player_speed = 5

# Set up the maze grid
grid_size = 50  # Each grid cell will be a 50x50 square
maze_width = width // grid_size
maze_height = height // grid_size

# Create a simple maze using a grid (1 for wall, 0 for path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Set up the obstacles based on the maze grid
obstacles = []
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == 1:  # Check correctly
            obstacle_x = col * grid_size
            obstacle_y = row * grid_size
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, grid_size, grid_size))

# Set up the clock for FPS
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Update player's position based on keys pressed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed

    # Ensure the player stays within the window boundaries
    player_x = max(player_radius, min(player_x, width - player_radius))
    player_y = max(player_radius, min(player_y, height - player_radius))

    # Create a rectangle for the player
    player_rect = pygame.Rect(player_x - player_radius, player_y - player_radius, player_radius * 2, player_radius * 2)

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            # If there is a collision, push the player back in the opposite direction
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x += player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x -= player_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_y += player_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_y -= player_speed

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the obstacles (maze walls)
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)

    # Draw the player (circle)
    pygame.draw.circle(screen, RED, (player_x, player_y), player_radius)

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
