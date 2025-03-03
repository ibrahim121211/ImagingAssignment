import pygame
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 500
FPS = 60
MOVE_SPEED = 200  # Pixels per second (frame rate independent)
SCALE = 3  # Scale factor to enlarge the character
WHITE = (255, 255, 255)

# Load sprite sheet
sprite_sheet = pygame.image.load("Assets/player.png")

# Define sprite size
SPRITE_WIDTH, SPRITE_HEIGHT = 24, 24
SPRITE_OFFSET_X, SPRITE_OFFSET_Y = 12, 20

# Function to extract and scale sprites
def get_scaled_sprites(start_y):
    return [
        pygame.transform.scale(
            sprite_sheet.subsurface(pygame.Rect((i * 2) * SPRITE_WIDTH + SPRITE_OFFSET_X, start_y + SPRITE_OFFSET_Y, SPRITE_WIDTH, SPRITE_HEIGHT)),
            (SPRITE_WIDTH * SCALE, SPRITE_HEIGHT * SCALE)
        )
        for i in range(6)
    ]

# Define animation frames for each direction
ANIMATIONS = {
    "idle_down": get_scaled_sprites(0),
    "idle_right": get_scaled_sprites(2 * SPRITE_HEIGHT),
    "idle_up": get_scaled_sprites(4 * SPRITE_HEIGHT),
    "idle_left": [pygame.transform.flip(frame, True, False) for frame in get_scaled_sprites(2 * SPRITE_HEIGHT)],
    "walk_down": get_scaled_sprites(6 * SPRITE_HEIGHT),
    "walk_right": get_scaled_sprites(8 * SPRITE_HEIGHT),
    "walk_up": get_scaled_sprites(10 * SPRITE_HEIGHT),
    "walk_left": [pygame.transform.flip(frame, True, False) for frame in get_scaled_sprites(8 * SPRITE_HEIGHT)]
}

# Character class
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = MOVE_SPEED  # Pixels per second
        self.direction = "down"
        self.frame = 0
        self.moving = False
        self.image = ANIMATIONS[f"idle_{self.direction}"][0]
        self.anim_timer = 0  # Timer to track when to switch frames

        # Damage flash variables
        self.damage_flash_active = False
        self.damage_start_time = 0
        self.flash_duration = 0.8  # Total flash time in seconds
        self.flash_interval = 0.1  # Flash interval time in seconds

    def take_damage(self):
        """Triggers the damage flash effect."""
        self.damage_flash_active = True
        self.damage_start_time = time.time()

    def move(self, keys, deltaTime):
        self.moving = False
        move_amount = self.speed * deltaTime  # Frame-independent movement

        if keys[pygame.K_LEFT]:
            self.x -= move_amount
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.x += move_amount
            self.direction = "right"
            self.moving = True
        elif keys[pygame.K_UP]:
            self.y -= move_amount
            self.direction = "up"
            self.moving = True
        elif keys[pygame.K_DOWN]:
            self.y += move_amount
            self.direction = "down"
            self.moving = True

        # Select the correct animation type (idle/walk)
        anim_type = "walk" if self.moving else "idle"
        anim_list = ANIMATIONS[f"{anim_type}_{self.direction}"]
        anim_speed = 0.1  # Adjust animation speed

        # Update animation based on deltaTime
        self.anim_timer += deltaTime
        if self.anim_timer >= anim_speed:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(anim_list)

    def update(self):
        """Updates the character (including damage flash effect) while keeping animation playing."""
        anim_type = "walk" if self.moving else "idle"
        anim_list = ANIMATIONS[f"{anim_type}_{self.direction}"]
        self.image = anim_list[self.frame]  # Keep updating animation

        if self.damage_flash_active:
            elapsed_time = time.time() - self.damage_start_time
            if elapsed_time < self.flash_duration:
                alpha = 0 if int(elapsed_time / self.flash_interval) % 2 == 0 else 255
                self.image.set_alpha(alpha)  # Apply flashing effect
            else:
                self.damage_flash_active = False  # Stop flashing
                self.image.set_alpha(255)  # Reset transparency to normal
        else:
            self.image.set_alpha(255)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))



# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    character = Character(WIDTH // 2, HEIGHT // 2)

    while running:
        deltaTime = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                character.take_damage()

        keys = pygame.key.get_pressed()
        character.move(keys, deltaTime)
        character.update()  # Update damage flash effect
        character.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
