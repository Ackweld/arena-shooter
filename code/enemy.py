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
        self.direction = vector(0, -1)
        self.speed = 400

        # Objects that the player should collide with
        self.collision_sprites = collision_sprites
        
    def move(self, dt):
        print("MOVING")
        self.collision_rect.x += self.direction.x * self.speed * dt
        self.collison("horizontal")

        self.collision_rect.y += self.direction.y * self.speed * dt
        self.collison("vertical")

    def collison(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.collision_rect):
                if axis == "horizontal":
                    if (
                        self.collision_rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.collision_rect.left = sprite.rect.right
                    if (
                        self.collision_rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.collision_rect.right = sprite.rect.left
                else:  # vertical
                    if (
                        self.collision_rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.collision_rect.top = sprite.rect.bottom
                    if (
                        self.collision_rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.collision_rect.bottom = sprite.rect.top
        
    def update(self, dt):
        self.old_rect = self.collision_rect.copy()
        self.move(dt)
