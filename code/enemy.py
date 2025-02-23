from settings import *
from os.path import join


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        print(f"ENEMY STARTING POS: {pos}")
        # Load original image
        self.original_image = pygame.image.load(
            join("..", "graphics", "enemy", "enemy.png")
        ).convert_alpha()

        self.image = self.original_image.copy()

        # Collision rectangle (does NOT rotate)
        self.collision_rect = self.image.get_rect(center=pos)
        # Used to check from which direction the player came from before collision
        self.old_rect = self.collision_rect.copy()

        # The actual sprite rect (for rendering)
        self.rect = self.collision_rect.copy()

        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # Movement
        self.direction = vector()
        self.speed = 400

        # Objects that the player should collide with
        self.collision_sprites = collision_sprites
