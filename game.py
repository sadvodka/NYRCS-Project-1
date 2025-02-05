import pygame
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game with Two Players, Skills, and Health")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Player class with movement, skill, and health
class Player(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y, controls):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

        self.speed = 5
        self.health = 100  # Player's health
        self.skill_cooldown = 0.5 # seconds for skill cooldown
        self.last_skill_time = 0  # timestamp of the last skill usage
        self.controls = controls  # The key controls for the player

    def update(self):
        # Movement controls
        keys = pygame.key.get_pressed()
        if keys[self.controls['left']] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[self.controls['right']] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[self.controls['up']] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[self.controls['down']] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def use_skill(self):
        # Check cooldown
        current_time = time.time()
        if current_time - self.last_skill_time >= self.skill_cooldown:
            self.last_skill_time = current_time
            return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0


# Fireball class to represent the skill's projectile
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((50, 25))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # Slightly offset the fireball from the player
        self.rect.center = (x, y)

        self.speed = 10
        self.damage = 25  # Fireball damage value
        self.direction = direction  # direction of the fireball (1 for right, -1 for left)

    def update(self):
        # Move the fireball based on its direction
        self.rect.x += self.speed * self.direction
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()  # Remove the fireball if it goes off-screen


# Initialize players and groups
controls_player1 = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'skill': pygame.K_SPACE}
controls_player2 = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'skill': [pygame.K_LSHIFT, pygame.K_RSHIFT]}  # Support both shift keys

player1 = Player(BLUE, WIDTH // 4, HEIGHT // 2, controls_player1)
player2 = Player(YELLOW, 3 * WIDTH // 4, HEIGHT // 2, controls_player2)

all_sprites = pygame.sprite.Group()
all_sprites.add(player1, player2)

fireballs = pygame.sprite.Group()

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()

    # Update both players individually
    player1.update()
    player2.update()

    # Fire skill for player1 (spacebar) and player2 (shift)
    if keys[controls_player1['skill']] and player1.use_skill():  # Player 1 fires (right direction)
        fireball = Fireball(player1.rect.centerx + 100, player1.rect.centery, 1)  # Direction 1 for right, slight offset
        fireballs.add(fireball)
        all_sprites.add(fireball)

    # Player 2 fires if any shift key is pressed (left direction)
    if any(keys[shift_key] for shift_key in controls_player2['skill']) and player2.use_skill():  # Player 2 fires (left direction)
        fireball = Fireball(player2.rect.centerx - 100, player2.rect.centery, -1)  # Direction -1 for left, slight offset
        fireballs.add(fireball)
        all_sprites.add(fireball)

    # Update each sprite individually
    for sprite in all_sprites:
        sprite.update()

    # Collision detection: Check if any fireball hits Player 1 or Player 2
    for fireball in fireballs:
        if fireball.rect.colliderect(player1.rect):
            player1.take_damage(fireball.damage)
            fireball.kill()  # Remove the fireball after it hits Player 1

        if fireball.rect.colliderect(player2.rect):
            player2.take_damage(fireball.damage)
            fireball.kill()  # Remove the fireball after it hits Player 2

    # Draw all sprites
    all_sprites.draw(screen)

    # Display player health
    font = pygame.font.SysFont(None, 36)
    health_text1 = font.render(f"Player 1 Health: {player1.health}", True, YELLOW)
    screen.blit(health_text1, (10, 10))

    health_text2 = font.render(f"Player 2 Health: {player2.health}", True, YELLOW)
    screen.blit(health_text2, (WIDTH - 250, 10))

    # Update the screen
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

pygame.quit()
