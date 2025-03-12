import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Circle and Avoid Obstacles (Maze)")

# Pages
HOMEPAGE = 0
GAME = 1
WINGAME = 2
DIEGAME = 3
game_state = HOMEPAGE

# Font
font = pygame.font.Font(None, 20)

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW  = (255, 255, 0)
BLACK = (0, 0, 0)

# Set the player's attributes
player_radius = 20
player_x = 25
player_y = 75
player_speed = 5

# Set up the maze grid
grid_size = 50  # Each grid cell will be a 50x50 square
maze_width = width // grid_size
maze_height = height // grid_size

def draw_text(text, x, y, colour = BLACK):
    label = font.render(text, True, colour)
    screen.blit(label, (x, y))

# Create a simple maze using a grid (1 for wall, 0 for path)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 1],

]

# Set up the obstacles based on the maze grid
obstacles = []
endpts = []
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == 1:  # Check correctly
            obstacle_x = col * grid_size
            obstacle_y = row * grid_size
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, grid_size, grid_size))
        if maze[row][col] == 2:
            endpt_x = col * grid_size
            endpt_y = row * grid_size
            endpts.append(pygame.Rect(endpt_x, endpt_y, grid_size, grid_size))

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

    #Homepage

    if game_state == HOMEPAGE:
        draw_text("Maze Runner", width //3, height//4, BLUE)
        draw_text("Press Space to start", width//4, height//2)

        if keys[pygame.K_SPACE]:
            game_state = GAME

    elif game_state == GAME:

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

    # Check for collisions with endpt
        for endpt in endpts:
            if player_rect.colliderect(endpt):
                print("Collide")

    # Fill the screen with white
        screen.fill(WHITE)

    # Draw the obstacles (maze walls)
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLUE, obstacle)

    # Draw end point
        for endpt in endpts:
            pygame.draw.rect(screen, YELLOW, endpt)

    # Draw the player (circle)
        pygame.draw.circle(screen, RED, (player_x, player_y), player_radius)

    # Update the display
        pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()
